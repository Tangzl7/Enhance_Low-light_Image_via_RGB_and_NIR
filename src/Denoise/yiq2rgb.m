function rgb = yiq2rgb(rgbImage)
redChannel = double( rgbImage(:, :, 1));
greenChannel =  double(rgbImage(:, :, 2));
blueChannel = double( rgbImage(:, :, 3));

r=1*redChannel+0.9563*greenChannel+0.6210*blueChannel;
g=1*redChannel-0.2721*greenChannel-0.6474*blueChannel;
b=1*redChannel-1.1070*greenChannel+1.7046*blueChannel;

rgbImage(:, :, 1)=r;
rgbImage(:, :, 2)=g;
rgbImage(:, :, 3)=b;
rgb=rgbImage;
end