from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
old='<button id="joinWifi">📱 JOIN BY ADDRESS</button>'
assert old in s, "V428 join button not found"
s=s.replace(old,'<button id="joinWifi">🔎 FIND RACE</button><button id="joinAddressAdvanced" style="font-size:12px;opacity:.75">Advanced: Join by address</button>',1)
old="const ip=prompt('Enter host hotspot IP address (example: 192.168.43.1)');if(ip){FidgetMultiplayer.joinWifi(ip.trim(),42714);networkStatus('Connecting to '+ip+'...');}"
assert old in s,"Expected V428 join handler missing"
s=s.replace(old,"FidgetMultiplayer.findRace();networkStatus('Looking for nearby races on this Wi-Fi or hotspot...');",1)
needle="window.addEventListener('fidget-local-multiplayer',e=>"
assert needle in s
s=s.replace(needle,"$('joinAddressAdvanced').onclick=()=>{const ip=prompt('Host IP address');if(ip&&typeof FidgetMultiplayer!=='undefined')FidgetMultiplayer.joinWifi(ip.trim(),42714);};\n"+needle,1)
s=s.replace("else if(d.type==='connected'||", "else if(d.type==='discovered'){networkStatus('Race found! Connecting to '+d.message+'...');}else if(d.type==='connected'||",1)
s=s.replace("tap JOIN BY ADDRESS. Enter the host address shown.","tap FIND RACE. The game will search and connect automatically.",1)
p.write_text(s)
j=Path("android-project/app/src/main/java/com/fidgetracing/game/LocalMultiplayer.java")
s=j.read_text()
needle=' @JavascriptInterface public void joinWifi(String address,int port)'
assert needle in s
addon="""
 // Local network discovery only; no internet server required.
 final int discoveryPort=42715;
 volatile boolean advertising=false;
 void advertise(){
   if(advertising)return;advertising=true;
   pool.execute(()->{
     try(DatagramSocket sock=new DatagramSocket()){
       sock.setBroadcast(true);
       byte[] bytes="FIDGET_RACE_429:42714".getBytes("UTF-8");
       while(running&&hosting){
         try{
           sock.send(new DatagramPacket(bytes,bytes.length,InetAddress.getByName("255.255.255.255"),discoveryPort));
           java.util.Enumeration<NetworkInterface> nis=NetworkInterface.getNetworkInterfaces();
           while(nis.hasMoreElements()){
             NetworkInterface ni=nis.nextElement();
             for(InterfaceAddress ia:ni.getInterfaceAddresses()){
               InetAddress broadcast=ia.getBroadcast();
               if(broadcast!=null)sock.send(new DatagramPacket(bytes,bytes.length,broadcast,discoveryPort));
             }
           }
         }catch(Exception ignored){}
         Thread.sleep(1000);
       }
     }catch(Exception e){event("error","Race advertisement: "+e.getMessage());}
     finally{advertising=false;}
   });
 }
 @JavascriptInterface public void findRace(){
   pool.execute(()->{
     event("searching","Searching for a nearby host...");
     try(DatagramSocket socket=new DatagramSocket(null)){
       socket.setReuseAddress(true);
       socket.bind(new InetSocketAddress(discoveryPort));
       socket.setSoTimeout(10000);
       long deadline=System.currentTimeMillis()+10000;
       byte[] buf=new byte[128];
       while(running&&System.currentTimeMillis()<deadline){
         DatagramPacket packet=new DatagramPacket(buf,buf.length);
         try{socket.receive(packet);}catch(SocketTimeoutException timeout){break;}
         String msg=new String(packet.getData(),0,packet.getLength(),"UTF-8");
         if(msg.equals("FIDGET_RACE_429:42714")){
           String ip=packet.getAddress().getHostAddress();
           event("discovered",ip);
           joinWifi(ip,42714);
           return;
         }
       }
       event("error","No race found. Check both devices are on the same hotspot/Wi-Fi, then try again or use Advanced.");
     }catch(Exception e){event("error","Discovery: "+e.getMessage());}
   });
 }
"""
s=s.replace(needle,addon+needle,1)
s=s.replace('server=listener;event("hosting"', 'server=listener;advertise();event("hosting"',1)
j.write_text(s)
print("Applied Build 429 nearby race discovery, Find Race button, and advanced manual fallback.")
