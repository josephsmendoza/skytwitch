import sys.net.Host;
import sys.ssl.Socket;
using StringTools;

class SkyTwitch {
    static function main() {
        var socket:Socket=new Socket();
        socket.connect(new Host("irc.chat.twitch.tv"),6697);
        socket.output.writeString("pass " + Sys.args()[0] + "\n");
        socket.output.writeString("nick " + Sys.args()[1] + "\n");
        socket.output.writeString("join #" + Sys.args()[2] + "\n");
        while(true){
            var line=socket.input.readLine();
            Sys.stdout().writeString(line+"\n");
            Sys.stdout().flush();
            if(line.startsWith("PING ")){
                socket.output.writeString("PONG "+line.substring(5));
            }else{
                var index = line.indexOf("~");
                if(index!=-1){
                    Sys.command("sse",[line.substring(index+1)]);
                }
            }
        }
    }
}