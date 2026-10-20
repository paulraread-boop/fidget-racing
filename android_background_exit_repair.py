from pathlib import Path

# Apply lifecycle repair after unpacking the approved Android source.
# Keep the original approved game HTML, graphics and menus unchanged.
p = Path("android-project/app/src/main/java/com/fidgetracing/game/MainActivity.java")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("""package com.fidgetracing.game;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;

public class MainActivity extends Activity {
  private WebView web;
  @Override public void onCreate(Bundle b) {
    super.onCreate(b);
    web = new WebView(this);
    setContentView(web);
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setAllowFileAccess(true);
    s.setMediaPlaybackRequiresUserGesture(false);
    web.setWebViewClient(new WebViewClient());
    web.setWebChromeClient(new WebChromeClient());
    web.loadUrl("file:///android_asset/index.html");
  }
  @Override protected void onPause() {
    if (web != null) {
      web.evaluateJavascript("window.fidgetSuspend && window.fidgetSuspend()", null);
      web.onPause();
      web.pauseTimers();
    }
    super.onPause();
  }
  @Override protected void onResume() {
    super.onResume();
    if (web != null) {
      web.resumeTimers();
      web.onResume();
      web.evaluateJavascript("window.fidgetResume && window.fidgetResume()", null);
    }
  }
  @Override public void onBackPressed() {
    finish();
  }
  @Override protected void onDestroy() {
    if (web != null) {
      web.stopLoading();
      web.loadUrl("about:blank");
      web.onPause();
      web.removeAllViews();
      web.destroy();
      web = null;
    }
    super.onDestroy();
  }
}
""")
print("Background lifecycle and exit repair applied")

# The in-game Exit Game control returns to Fidget Racing's main screen,
# rather than closing the Android Activity. Preserve the original game.
html = Path("android-project/app/src/main/assets/index.html")
game = html.read_text(encoding="utf-8")
old = "if(window.Android&&typeof window.Android.exitApp==='function'){window.Android.exitApp();}"
if old not in game:
    raise SystemExit("Expected quit handler not found; refusing unsafe modification")
game = game.replace(old, "", 1)
game = game.replace('id="quit" aria-label="Quit race and return to menu">Quit</button>', 'id="quit" aria-label="Exit game and return to main menu">Exit Game</button>', 1)
html.write_text(game, encoding="utf-8")
print("Exit Game now stops race and returns to main menu without closing Android app")
