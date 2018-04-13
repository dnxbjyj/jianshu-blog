做项目的时候，需要使用到手写字体来让内容更加的美观。可是程序中默认使用的是系统的默认字体，怎么将TextView（或EditText）的字体设置成自己想要的字体呢？步骤如下：

* 下载字体文件(`.ttf`格式)，比如`Jinglei.ttf`（方正静蕾的字体文件），然后将其复制到项目工程的`assets/fonts`目录下。

* 设置TextView的字体：
```java
TextView tv = (TextView)findViewById(R.id.my_textview);
Typeface typeface = Typeface.createFromAsset(mContext.getAssets(), "fonts/Jinglei.ttf");  // mContext为上下文
tv.setTypeface(typeface );
```
* 为了使用起来方便，还可以将设置字体的操作封装成一个工具类：
```java
/**
 * 字体相关操作工具类
 * 
 */
public class TypefaceUtil {
    // 上下文
    private Context mContext;
    private Typeface mTypeface;

    /**
     * 如果ttfPath为null那么mTypeface就为系统默认值
     * 
     * @param context
     * @param ttfPath
     */

    public TypefaceUtil(Context context, String ttfPath) {
        mContext = context;
        mTypeface = getTypefaceFromTTF(ttfPath);
    }

    /**
     * 从ttf文件创建Typeface对象
     * 
     * @ttfPath "fonts/XXX.ttf"
     */
    public Typeface getTypefaceFromTTF(String ttfPath) {

        if (ttfPath == null) {
            return Typeface.DEFAULT;
        } else {
            return Typeface.createFromAsset(mContext.getAssets(), ttfPath);
        }
    }

    /**
     * 设置TextView的字体 
     * 
     * @tv TextView对象
     * @ttfPath ttf文件路径
     * @isBold 是否加粗字体
     */
    public void setTypeface(TextView tv, boolean isBold) {
        tv.setTypeface(mTypeface);
        setBold(tv, isBold);
    }

    /**
     * 设置字体加粗
     */
    public void setBold(TextView tv, boolean isBold) {
        TextPaint tp = tv.getPaint();
        tp.setFakeBoldText(isBold);
    }

    /**
     * 设置TextView的字体为系统默认字体
     * 
     */
    public void setDefaultTypeFace(TextView tv, boolean isBold) {
        tv.setTypeface(Typeface.DEFAULT);
        setBold(tv, isBold);
    }

    /**
     * 设置当前工具对象的字体
     * 
     */
    public void setmTypeface(String ttfPath) {
        mTypeface = getTypefaceFromTTF(ttfPath);
    }

}
```
* 使用的时候只需这样调用：
```java
TypefaceUtil tfUtil = new TypefaceUtil(mContext,"fonts/Jinglei.ttf");
tfUtil.setTypeface(tv,false);
```









