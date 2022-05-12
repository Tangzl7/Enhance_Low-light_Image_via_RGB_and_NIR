function variance = Variance(img_path)
i=imread(img_path); %载入真彩色图像
i=rgb2gray(i); %转换为灰度图
i=double(i);  %将uint8型转换为double型，否则不能计算统计量
% sq1=var(i,0,1); %列向量方差，第二个参数为0，表示方差公式分子下面是n-1,如果为1则是n
% sq2=var(i,0,2); %行向量方差
avg=mean2(i);  %求图像均值
[m,n]=size(i);
s=0;
for x=1:m
    for y=1:n
    s=s+(i(x,y)-avg)^2; %求得所有像素与均值的平方和。
    end
end
%求图像的方差
variance=var(i(:));