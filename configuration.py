from pathlib import Path
import datetime
class Configuration(object):

    z_dim = 32
    # Architecture
    d_n_conv_modules =  4 # number of conv. modules
    n_conv_layers_per_module = 1 # number of conv. layers in each module (between each pool layer/dim reduction)
    n_dense_layers = 2 # number of dense layers in 
    n_dense_units = z_dim
    # put config variable definitions here
    n_epochs = 100
    dataset = 'mnist'
    n_train = 100
    n_val = 50
    n_test = 100
    n_test_in = 50
    out_frac = (n_test-n_test_in)/n_test
    train_batch_size = 64
    if dataset in ('dreyeve','prosivic'):
        image_height = 256
        image_width = 256
        channels = 3
        batch_size = 64
    elif dataset in ('mnist','mnist_vs_omniglot'):
        image_height = 28
        image_width = 28
        channels = 1
        batch_size = 128
        n_test = 5000
        n_test_in = 2500

    architecture = None
    # architecture = "0_5_0_8_512_5_2_2"
    if dataset == 'mnist':
        architecture = 'ALOCC_mnist'
    max_pool = False
    use_batch_norm = True
    use_dropout = False
    dropout_rate = 0.1
    experiment_name = 'debug'
    time_stamp = datetime.datetime.now().strftime("%y_%m_%d_kl%H_%M")

    
    # test settings
    load_epoch = n_epochs-1
    test_batch_size = 64
    # generated config settings
    log_dir = './log/'+dataset+'/'+experiment_name+'/'
    model_dir = log_dir+'models/'
    train_dir = log_dir+'train/'
    test_dir = log_dir+'test/'
    test_batch_verbose = False

    # dataset specific options below

    if dataset == "dreyeve":
        img_folder =   "../weather_detection_data/dreyeve/highway_morning_sunny_vs_rainy/"
        train_folder = "../weather_detection_data/dreyeve/highway_morning_sunny_vs_rainy/train/"
        val_folder =   "../weather_detection_data/dreyeve/highway_morning_sunny_vs_rainy/val/"
        test_in_folder =  "../weather_detection_data/dreyeve/highway_morning_sunny_vs_rainy/test/out/"
        test_out_folder =  "../weather_detection_data/dreyeve/highway_morning_sunny_vs_rainy/test/out/"
    
    elif dataset == "prosivic":
        img_folder =   "../weather_detection_data/prosivic/"
        train_folder = "../weather_detection_data/prosivic/train/"
        val_folder =   "../weather_detection_data/prosivic/val/"
        test_in_folder =  "../weather_detection_data/prosivic/test/in/"
        test_out_folder =  "../weather_detection_data/prosivic/test/out/"


    elif dataset == "bdd100k":
        img_folder = Path("/data/bdd100k/images/train_and_val_256by256")
        norm_file = "/data/bdd100k/namelists/clear_or_partly_cloudy_or_overcast_and_highway_and_daytime.txt"
        norm_filenames = loadbdd100k.get_namelist_from_file(norm_file)
        out_file = "/data/bdd100k/namelists/rainy_or_snowy_or_foggy_and_highway_and_daytime_or_dawndusk_or_night.txt"
        out_filenames = loadbdd100k.get_namelist_from_file(out_file)
        norm_spec = [["weather", ["clear","partly cloudy", "overcast"]],["scene", "highway"],["timeofday", "daytime"]]
        out_spec = [["weather", ["rainy", "snowy", "foggy"]],["scene", "highway"],["timeofday",["daytime","dawn/dusk","night"]]]
        save_name_lists=False
        labels_file = None
        get_norm_and_out_sets = False
        shuffle=False
        architecture = "b1"
    

    # Dataset specific parameters below

