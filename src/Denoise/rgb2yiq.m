function yiq = rgb2yiq(rgbImage)

redChannel =double( rgbImage(:, :, 1));
greenChannel =  double(rgbImage(:, :, 2));
blueChannel = double( rgbImage(:, :, 3));

y=0.299*redChannel+0.587*greenChannel+0.114*blueChannel;
i=0.595716*redChannel-0.274453*greenChannel-0.321263*blueChannel;
q=0.211456*redChannel-0.522591*greenChannel+0.311135*blueChannel;

rgbImage(:, :, 1)=y;
rgbImage(:, :, 2)=i;
rgbImage(:, :, 3)=q;
yiq=rgbImage;
end