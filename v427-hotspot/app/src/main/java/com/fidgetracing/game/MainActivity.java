package com.fidgetracing.game;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.*;
public class MainActivity extends Activity {
 WebView web; LocalMultiplayer localMultiplayer; NativeRaceBridge nativeRace;
 public class AndroidBridge { @JavascriptInterface public void exitApp(){runOnUiThread(()->finishAndRemoveTask());} }
 @Override public void onCreate(Bundle b){super.onCreate(b);web=new WebView(this);setContentView(web);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(true);s.setMediaPlaybackRequiresUserGesture(false);web.addJavascriptInterface(new AndroidBridge(),"FidgetAndroid");localMultiplayer=new LocalMultiplayer(this,web);web.addJavascriptInterface(localMultiplayer,"FidgetMultiplayer");nativeRace=new NativeRaceBridge(this,web,localMultiplayer);web.addJavascriptInterface(nativeRace,"NativeRace");web.setWebViewClient(new WebViewClient());web.setWebChromeClient(new WebChromeClient());web.loadUrl("file:///android_asset/index.html");}
 @Override public void onDestroy(){if(localMultiplayer!=null)localMultiplayer.close();super.onDestroy();}
}