import json
import os
import math

# A default attribute value set for some NFTs missing certain attributes
DEFAULT_VALUE = "none-404-null"

class NftRarityTool:

    # raw_data and nft_attrs are duplicate data
    # the code is not clean but considering NFT metadata size are small
    # and convenience to use intermediate results
    # let's keep it this way
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.raw_data = []
        self.nft_attrs = {}
        self.nft_score = {}
        self.all_attr_names = set()

    # load all data in data_dir
    # expect each line to be a valid json
    def __load_data(self):
        # considering most NFT ares between 3000 - 10000
        # we will just load everything into memory

        res = []
        f_l = os.listdir(self.data_dir)

        for f_n in f_l:
            with open(self.data_dir + "/" + f_n) as f_r:
                for l in f_r.readlines():
                    l_clean = l.strip('\n')
                    res.append(json.loads(l_clean))

        self.raw_data = res

    # extract all attribute fields for each token
    # Attribute looks like (attr_name, attr_value) pair
    # to make it easier to compare we transform it as attr_name_attr_value string
    # If some attribute is missing some attributes, we set a default value for it
    #
    # After transform, each NFT will get a fixed length vector of all attributes
    def __data_transform(self, raw_data_vec):
        # first pass get all attrs
        for each_data in raw_data_vec:
            data_attrs = each_data['attributes']
            for each_attr in data_attrs:
                self.all_attr_names.add(each_attr['trait_type'])

        for each_data in raw_data_vec:
            data_attrs = each_data['attributes']
            # when we fetch metadata we always have an id field set
            token_id = each_data['id']
            trans_res = []
            curr_attr_names = set()
            for each_attr in data_attrs:
                curr_attr_names.add(each_attr['trait_type'])
                trans_res.append(each_attr['trait_type'] + "_" + str(each_attr['value']))

            for missing_attr in self.all_attr_names.difference(curr_attr_names):
                trans_res.append(missing_attr + "_" + DEFAULT_VALUE)
            self.nft_attrs[token_id] = trans_res

    # We are borrowing from TF-IDF here mostly IDF is used
    def __calc_scores(self):
        total_count = len(self.nft_attrs)
        each_v_count = {}

        for each_token_attrs in self.nft_attrs.values():
            for each_attr in each_token_attrs:
                if each_attr in each_v_count:
                    each_v_count[each_attr] = each_v_count[each_attr] + 1
                else:
                    each_v_count[each_attr] = 1

        for (t_id, each_token_attrs) in self.nft_attrs.items():
            score = 0
            for each_attr in each_token_attrs:
                score += math.log(total_count / (each_v_count[each_attr] + 1))
            self.nft_score[t_id] = score

    def get_scores_in_desc(self):
        # load all data
        self.__load_data()
        # perform data transform
        self.__data_transform(self.raw_data)
        # calculate all scores
        self.__calc_scores()

        return sorted(self.nft_score.items(), key=lambda kv: kv[1], reverse=True)