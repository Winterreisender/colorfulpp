#include <gtest/gtest.h>
#include <iostream>
import colorfulpp;
using namespace colorfulpp;
using namespace std;

TEST(HelloTest, BasicAssertions) {


  auto color = RgbaColor(0x39, 0xc5, 0xbb, 0.5);
  auto hsvColor = HsvaColor::from(color.to_nrgba());
  EXPECT_STREQ(color.to_string().c_str(),"rgba(57,197,187,0.5)");

  cout << color.to_string() << endl;
  cout << color.to_nrgba().to_string() << endl;
  cout << HsvaColor::from( color.to_nrgba() ).to_string() << endl;
  cout << HsvaColor::from( color.to_nrgba() ).to_nrgba().to_string() << endl ;

  cout << HexaColor::from( color.to_nrgba() ).to_string() << endl ;

  EXPECT_TRUE( 
    color.to_nrgba() == HsvaColor::from( color.to_nrgba() ).to_nrgba() 
  );
}