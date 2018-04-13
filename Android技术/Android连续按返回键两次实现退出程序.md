思路：重写`Activity`的`onKeyDown`方法，判断按键是不是返回键，如果是，则再判断按下的时间和上次按下的时间之间的差值（毫秒数）是不是大于2000，如果不大于，则用`finish()`方法结束程序。Demo如下：
```java
import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.widget.Toast;
 
public class TestActivity extends Activity {
        private long mExitTime;  //存在时间，初值为0，用于和当前时间（毫秒数）做差值
     
    @Override
        public void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                setContentView(R.layout.main);
 
        }
    
    @Override     
        public boolean onKeyDown(int keyCode, KeyEvent event) {
                if (keyCode == KeyEvent.KEYCODE_BACK) {
                        if ((System.currentTimeMillis() - mExitTime) > 2000) {  //mExitTime的初始值为0，currentTimeMillis()肯定大于2000（毫秒），所以第一次按返回键的时候一定会进入此判断
21                                 Toast.makeText(this, "再按一次退出程序", Toast.LENGTH_SHORT).show();
                                mExitTime = System.currentTimeMillis();
 
                        } else {
                                finish();
                        }
                        return true;
                }
                return super.onKeyDown(keyCode, event);
        }
}
```
