import haxe.Timer;
import sys.net.Host;
import sys.net.Socket;
import sys.io.File;
import haxe.Json;
import haxe.Http;

using StringTools;

class SkyTwitch {
	static var config:Config;

	static function main() {
		config = Json.parse(File.getContent("config.json"));
		var socket:Socket = new Socket();
		socket.connect(new Host(config.host), config.port);
		socket.output.writeString("pass " + config.pass + "\n");
		socket.output.writeString("nick " + config.user + "\n");
		socket.output.writeString("join #" + config.channel + "\n");
		if (config.givePointTime != null && config.givePointTime > 0) {
			new Timer(config.givePointTime * 1000).run = function() {
				var chatters:Chatters = Json.parse(Http.requestUrl("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters"));
				for (user in chatters.chatters.viewers) {
					config.users[user]++;
				}
			}
		}
		while (true) {
			var line = socket.input.readLine();
			Sys.stdout().writeString(line + "\n");
			Sys.stdout().flush();
			if (line.startsWith("PING ")) {
				var pong = "PONG " + line.substring(5) + "\n";
				Sys.stdout().writeString(pong);
				socket.output.writeString(pong);
			} else {
				var index = line.indexOf("~");
				if (index != -1) {
					Sys.command("sse", [line.substring(index + 1)]);
				}
			}
		}
	}
}
