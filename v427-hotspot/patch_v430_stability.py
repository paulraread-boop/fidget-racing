from pathlib import Path
p=Path("android-project/app/src/main/java/com/fidgetracing/game/LocalMultiplayer.java")
s=p.read_text()
needle=' @JavascriptInterface public void joinWifi(String address,int port)'
assert needle in s
start=s.index(needle)
end=s.index(' @JavascriptInterface public void send(',start)
replacement=''' @JavascriptInterface public void joinWifi(String address,int port){
   if(address==null||address.trim().isEmpty()){event("error","No host address");return;}
   final String hostAddress=address.trim();
   pool.execute(()->{
     if(port<1024||port>65535){event("error","Invalid port");return;}
     hosting=false;
     int failures=0;
     while(running&&!hosting){
       try(Socket connection=new Socket()){
         client=connection;
         connection.connect(new InetSocketAddress(hostAddress,port),8000);
         connection.setKeepAlive(true);
         connection.setTcpNoDelay(true);
         failures=0;
         link(connection,0);
         if(running&&!hosting)event("reconnecting","Connection lost; reconnecting...");
       }catch(Exception e){
         if(running&&!hosting)event("reconnecting","Connection interrupted; retrying...");
       }finally{client=null;writer=null;}
       if(!running||hosting)break;
       failures++;
       try{Thread.sleep(Math.min(5000,1000L*failures));}catch(InterruptedException e){Thread.currentThread().interrupt();break;}
     }
   });
 }
'''
s=s[:start]+replacement+s[end:]
# TCP keepalive alone can take hours; app-level heartbeat keeps idle connections alive.
needle=' void link(Socket s,int id)throws IOException{'
assert needle in s
s=s.replace(needle,''' void link(Socket s,int id)throws IOException{
   s.setKeepAlive(true);
   s.setTcpNoDelay(true);
''',1)
needle='while(running&&(line=in.readLine())!=null){if(line.length()>65536)break;'
assert needle in s
s=s.replace(needle,'while(running&&(line=in.readLine())!=null){if("__FIDGET_PING__".equals(line)){out.println("__FIDGET_PONG__");continue;}if("__FIDGET_PONG__".equals(line))continue;if(line.length()>65536)break;',1)
needle=' @JavascriptInterface public void send(String data)'
assert needle in s
s=s.replace(needle,''' @JavascriptInterface public void startHeartbeat(){
   pool.execute(()->{
     while(running){
       try{Thread.sleep(5000);}catch(InterruptedException e){Thread.currentThread().interrupt();return;}
       if(hosting){for(PrintWriter w:guests.values())w.println("__FIDGET_PING__");}
       else if(writer!=null)writer.println("__FIDGET_PING__");
     }
   });
 }
'''+needle,1)
p.write_text(s)
# Launch heartbeat once from Android bridge, preserving other behavior.
a=Path("android-project/app/src/main/java/com/fidgetracing/game/MainActivity.java")
t=a.read_text()
needle='web.addJavascriptInterface(localMultiplayer,"FidgetMultiplayer");'
assert needle in t
t=t.replace(needle,needle+'localMultiplayer.startHeartbeat();',1)
a.write_text(t)
print("Build 430: heartbeat and automatic reconnect added to existing network bridge.")
