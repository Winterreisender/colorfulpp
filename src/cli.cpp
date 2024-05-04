#include <iostream>
#include <unistd.h>

import colorfulpp;
using namespace std;
using namespace colorfulpp;

int main(int argc, char* argv[]) {
    int o;
    const char *optstring = "hi:"; // 有三个选项-abc，其中c选项后有冒号，所以后面必须有参数
    RgbaColor color(0,0,0,0);
    while ((o = getopt(argc, argv, optstring)) != -1) {
        switch (o) {
            case 'i':
                color = *(RgbaColor::from_string(string(optarg)));
                cout << color.to_nrgba().to_string() << endl;
                cout << HsvaColor::from(color.to_nrgba()).to_string() << endl;
                cout << HexaColor::from(color.to_nrgba()).to_string() << endl;
                break;
            case 'h':
                printf("Example: %s -i rgba(10,20,30,0.5)\n", argv[0],optarg);
                
                break;
            default:
                printf("unknown argument: %c\n", optopt);
        }
    }
    return 0;
}