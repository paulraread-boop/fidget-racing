package com.fidgetracing.game;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.view.WindowManager;
import android.view.View;
public class MainActivity extends Activity {
 WebView web;
 @Override public void onCreate(Bundle b){ super.onCreate(b); getWindow().setFlags(1024,1024); getWindow().getDecorView().setSystemUiVisibility(5894|1024|512); web=new WebView(this); web.setBackgroundColor(0xff05091d); WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true); web.setWebChromeClient(new android.webkit.WebChromeClient()); setContentView(web); web.loadUrl("file:///android_asset/game.html"); }
 @Override public void onBackPressed(){ if(web!=null && web.canGoBack())web.goBack();else super.onBackPressed(); }
}
