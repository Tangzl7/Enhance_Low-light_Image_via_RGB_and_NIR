function entropy = Entropy(img_path)
I=imread(img_path);
[C,L]=size(I);
Img_size=C*L;
G=256;
H_x1=0;
nk=zeros(G,1);
for i=1:C
    for j=1:L
        Img_level=I(i,j)+1;
        nk(Img_level)=nk(Img_level)+1;
    end
end
for k=1:G
    Ps(k)=nk(k)/Img_size;
    if Ps(k)~=0;
        entropy=-Ps(k)*log2(Ps(k))+H_x1;
    end
end