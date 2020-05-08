import yaml


# =====================================================================================================================
class Config(object):

    def __init__(self, path):
        with open(path, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        self.puncture_tpl_file = cfg["puncture_tpl_file"]
        self.gui = cfg["gui"]
        self.trace = cfg["trace"]
        self.kernel_shape = cfg["kernel_shape"]
        self.kernel_size = cfg["kernel_size"]
        self.match_method = cfg["match_method"]
        self.center_fill_size = cfg["center_fill_size"]
        self.hough_threshold = cfg["hough_threshold"]
        self.probabilistic = cfg["probabilistic"]
        self.groups_min_distance = cfg["groups_min_distance"]
        self.max_gab_tolerance = cfg["max_gab_tolerance"]
        self.result_compare_tolerance = cfg["result_compare_tolerance"]
        self.symmetrize_tolerance = cfg["symmetrize_tolerance"]
# =====================================================================================================================