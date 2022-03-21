function enhanced_img = ELL(img_path, nir_path, write_path)
img = im2double(imread(img_path));
nir = im2double(imread(nir_path));
illummap = max(img, [], 3);
imwrite(illummap, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/init_illumination.png')
illummap_signal = wlsFilter(illummap);
illummap = wlsFilter_dul(illummap, illummap_signal, nir, 1);
imwrite(illummap, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/illumination.png')

enhanced_img = img ./ (illummap .^ 0.7);
imwrite(enhanced_img, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/init_enhancement.png')

enhanced_img_r = adapthisteq(enhanced_img(:,:,1), 'clipLimit',0.02,'Distribution','rayleigh');
enhanced_img_g = adapthisteq(enhanced_img(:,:,2), 'clipLimit',0.02,'Distribution','rayleigh');
enhanced_img_b = adapthisteq(enhanced_img(:,:,3), 'clipLimit',0.02,'Distribution','rayleigh');
enhanced_img(:, :, 1) = enhanced_img_r;
enhanced_img(:, :, 2) = enhanced_img_g;
enhanced_img(:, :, 3) = enhanced_img_b;
imwrite(enhanced_img, write_path);
