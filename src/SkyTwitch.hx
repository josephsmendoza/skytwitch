import haxe.Timer;
import sys.net.Host;
import sys.net.Socket;
import sys.io.File;
import haxe.Json;
import haxe.Http;
import haxe.Exception;

using StringTools;

class SkyTwitch {
	static var config:Config;

	static function main() {
		config = Json.parse(File.getContent("config.json"));
		var socket:Socket = new Socket();
		socket.connect(new Host(config.host), config.port);
		socket.output.writeString("pass " + config.pass + "\r\n");
		socket.output.writeString("nick " + config.user + "\r\n");
		socket.output.writeString("join #" + config.channel + "\r\n");
		socket.output.flush();
		if (config.givePointTime > 0) {
			new Timer(config.givePointTime * 1000).run = function() {
				var chatters:Chatters = Json.parse(Http.requestUrl("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters"));
				for (user in chatters.chatters.viewers) {
					trace("give point to " + user);
					config.users[user]++;
				}
				var out=File.write("config.json");
				out.writeString(Json.stringify(chatters));
				out.flush();
			}
		}
		while (true) {
			var line=socket.input.readLine();
			Sys.stdout().writeString(line + "\n");
			if (line.startsWith("PING ")) {
				var pong = "PONG " + line.substring(5);
				Sys.stdout().writeString(pong+"\n");
				socket.output.writeString(pong+"\r\n");
			} else {
				var index = line.indexOf("~");
				if (index != -1) {
					var command = line.substring(index + 1);
					if (command == "help") {
						var help="PRIVMSG ";
						if(config.game.toLowerCase().startsWith("skyrim")){
							help+="www.skyrimcommands.com";
						}else{
							help+="www.falloutcheats.com";
						}
						socket.output.writeString(help+"\r\n");
					} else {
						Sys.command("sse", [command]);
					}
				}
			}
			Sys.stdout().flush();
			socket.output.flush();
		}
	}
}
