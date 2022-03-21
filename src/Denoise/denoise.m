function OUT = denoise(I0_path, G_path, write_path)
% Zheng Junxue simulate paper:ENHANCING LOW LIGHT IMAGES USING NEAR INFRARED FLASH IMAGES
% Shaojie Zhuo, Xiaopeng Zhang, Xiaoping Miao, and
% Terence Sim, “Enhancing low light images using near infrared flash images,” 
% in 2010 IEEE International Conference on Image Processing. IEEE, 2010, pp. 2537–2540
% clear
I0 = im2double(imread(I0_path));
% yiq=rgb2yiq(I0);
% figure,imshow(yiq);
% figure,imshow(yiq2rgb(yiq));
G = im2double(imread(G_path));

tic
G = G(:,:,1);

GW=wlsFilter(G);
n_d=G./(GW+0.0001);
imwrite(n_d, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/detail.png')
lambda=1;
alpha=2;
i1=wlsFilter(I0(:,:,1),lambda);
i2=wlsFilter(I0(:,:,2),lambda);
i3=wlsFilter(I0(:,:,3),lambda);
in=cat(3,i1,i2,i3);
imwrite(in, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/base.png')
V_b=rgb2yiq(in);

V_l=V_b(:,:,1);

I0_l=rgb2yiq(I0);

V_l_nir=wlsFilter_dul(I0_l(:,:,1),V_l,G,lambda);
imwrite(V_l_nir, 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/noise_reduce.png')

%figure,imshow(V_l)
%figure,imshow(V_l_nir)
% figure,imshow(V_l_nir.*n_d)
% figure,imshow(V_l_nir+n_d)
OUT=yiq2rgb(cat(3,V_l_nir.*n_d,V_b(:,:,2),V_b(:,:,3)));
imwrite(OUT, write_path);
%figure,imshow(yiq2rgb(yiq))

%yiq_wls=cat(3,V_l.*n_d,V_b(:,:,2),V_b(:,:,3));
%toc
%figure,imshow(yiq2rgb(yiq_wls))

