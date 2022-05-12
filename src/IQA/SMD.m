function smd = SMD(img_path)
I = imread(img_path);
I = double(I);
[M, N] = size(I);
smd = 0;
for x = 1 : M-1
    for y = 2 : N-1
        % x方向和y方向的相邻像素灰度值之差的的平方和作为清晰度值
        smd = smd + abs(I(x,y)-I(x,y-1)) + abs(I(x,y)-I(x+1,y));
    end
end

