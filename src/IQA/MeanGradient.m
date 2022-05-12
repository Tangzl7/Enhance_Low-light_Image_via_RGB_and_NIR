function mean_gradient = MeanGradient(path)
img = imread(path);
img = double(img);
[r,c,b] = size(img);

dx = 1;
dy = 1;
for k = 1 : b
    band = img(:,:,k);
    [dzdx,dzdy] = gradient(band,dx,dy);
    s = sqrt((dzdx .^ 2 + dzdy .^2) ./ 2);
    g(k) = sum(sum(s)) / ((r - 1) * (c - 1));
end
mean_gradient = mean(g);

