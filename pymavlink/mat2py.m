data = [0, 0, 0];
 
host = '127.0.0.1';
port = 801;
 
u = udp(host,port);

for i = 1:10
    data(1) = data(1) + 1
    fopen(u);
    fwrite(u, data, 'double');
    fclose(u)
    pause(1)
end