import sys.net.Host;
import sys.net.Socket;
using StringTools;

class SkyTwitch {
    static function main() {
        var socket:Socket=new Socket();
        socket.connect(new Host("irc.chat.twitch.tv"),6667);
        socket.output.writeString("pass " + Sys.args()[0] + "\n");
        socket.output.writeString("nick " + Sys.args()[1] + "\n");
        socket.output.writeString("join #" + Sys.args()[2] + "\n");
        while(true){
            var line=socket.input.readLine();
            Sys.stdout().writeString(line+"\n");
            Sys.stdout().flush();
            if(line.startsWith("PING ")){
                var pong="PONG "+line.substring(5)+"\n"
                Sys.stdout().writeString(pong);
                socket.output.writeString(pong);
            }else{
                var index = line.indexOf("~");
                if(index!=-1){
                    Sys.command("sse",[line.substring(index+1)]);
                }
            }
        }
    }
}