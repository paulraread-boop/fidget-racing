package com.fidgetracing.game;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.JavascriptInterface;
public class MainActivity extends Activity {
  WebView web;
  public class AndroidBridge { @JavascriptInterface public void exitApp() { runOnUiThread(() -> finishAndRemoveTask()); } }
  @Override public void onCreate(Bundle b) { super.onCreate(b);
    web = new WebView(this); getWindow().getDecorView().setSystemUiVisibility(android.view.View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | android.view.View.SYSTEM_UI_FLAG_FULLSCREEN | android.view.View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE | android.view.View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
    setContentView(web);
    WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setAllowFileAccess(true); s.setMediaPlaybackRequiresUserGesture(false);
    web.addJavascriptInterface(new AndroidBridge(), "FidgetAndroid");
    web.setWebViewClient(new WebViewClient()); web.setWebChromeClient(new WebChromeClient());
    web.getSettings().setUseWideViewPort(true); web.getSettings().setLoadWithOverviewMode(true); web.loadUrl("file:///android_asset/index.html");
  }
  @Override protected void onPause(){ if(web!=null)web.onPause(); super.onPause(); }
  @Override protected void onResume(){ super.onResume(); if(web!=null)web.onResume(); }
  @Override protected void onDestroy(){ if(web!=null){web.stopLoading();web.loadUrl("about:blank");web.destroy();web=null;} super.onDestroy(); }
  @Override public void onBackPressed(){ if(web!=null)web.evaluateJavascript("(function(){if(typeof quitRace==='function')quitRace();})()",null); else super.onBackPressed(); }
}