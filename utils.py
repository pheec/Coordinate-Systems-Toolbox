def get_frame_names(transformation_name):
    str1, str2 = transformation_name.split('_to_')
    prefix = "T_"
    if str1.startswith(prefix):
        str1 = str1[len(prefix):]
    else:
        str1 = str1
    return str1, str2
