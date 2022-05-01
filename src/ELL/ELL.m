function enhanced_img = ELL(img_path, nir_path, write_path)
img = im2double(imread(img_path));
nir = im2double(imread(nir_path));
illummap = max(img, [], 3);
imwrite(illummap, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/init_illumination.png')
illummap_signal = wlsFilter(illummap);
illummap = wlsFilter_dul(illummap, illummap_signal, nir, 1);
imwrite(illummap, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/illumination.png')

enhanced_img = img ./ (illummap .^ 0.7);
imwrite(enhanced_img, write_path);
