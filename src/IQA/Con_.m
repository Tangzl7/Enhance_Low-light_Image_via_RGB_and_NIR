function CON = Con_(img_path)
I=imread(img_path);
CON=0;
[n, m]=size(I);
Lc = 4*(n-2)*(m-2)+2*(m-2)*3+2*(n-2)*3+4*2;
a = ones(n+2, m+2);
a = -a;
for i= 2:n+1
    for j= 2:m+1
        a(i, j) = I(i-1, j-1);
    end
end
dir = [1,0; 0,1; 0,-1; -1,0];
for i= 2:n+1
    for j= 2:m+1
        for k = 1:4
            x = i + dir(k, 1);
            y = j + dir(k, 2);
            cnt = a(x, y);
            if (cnt ~= -1)
                CON = CON + (cnt-a(i,j))*(cnt-a(i,j));
            end
        end
    end
end
CON = CON/Lc;