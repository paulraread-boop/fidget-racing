package com.fidgetracing.game;
import android.app.Activity;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import org.json.JSONObject;
public final class NativeRaceBridge {
 final Activity activity;final WebView web;final LocalMultiplayer transport;
 NativeRaceBridge(Activity a,WebView w,LocalMultiplayer t){activity=a;web=w;transport=t;}
 void onTransport(String type,String message){if("message".equals(type)){try{JSONObject j=new JSONObject(message);String js="window.dispatchEvent(new CustomEvent('fidget-native-race',{detail:"+j.toString()+"}));";activity.runOnUiThread(()->web.evaluateJavascript(js,null));}catch(Exception ignored){}}}
 @JavascriptInterface public void sendState(String state){transport.send(state);}
 @JavascriptInterface public void hostWifi(int port){transport.hostWifi(port);}
 @JavascriptInterface public void joinWifi(String address,int port){transport.joinWifi(address,port);}
}