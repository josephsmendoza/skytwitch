import sys.FileSystem;
import sys.thread.Thread;
import sys.net.Host;
import sys.net.Socket;
import sys.io.File;
import haxe.Http;
import haxe.Exception;
import haxe.Json;
import json2object.JsonParser;

using StringTools;

class SkyTwitch {
	static var config = new Config();
	static var socket = new Socket();

	static function main() {
		if (FileSystem.exists("config.json")) {
			config = new JsonParser<Config>().fromJson(File.getContent("config.json"));
		} else {
			var out = File.write("config.json");
			out.writeString(Json.stringify(config, "\t"));
			out.flush();
		}
		socket.connect(new Host(config.host), config.port);
		socket.output.writeString("pass " + config.pass + "\r\n");
		socket.output.writeString("nick " + config.user + "\r\n");
		socket.output.writeString("join #" + config.channel + "\r\n");
		socket.output.flush();
		if (config.givePointTime > 0) {
			Thread.create(function() {
				while (true) {
					var chatters:Chatters = Json.parse(Http.requestUrl("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters"));
					trace("there are " + chatters.chatters.viewers.length + " viewers");
					for (user in chatters.chatters.viewers.iterator()) {
						trace("give point to " + user);
						if (config.users.exists(user)) {
							config.users[user]++;
						} else {
							config.users.set(user, 1);
						}
					}
					var out = File.write("config.json");
					out.writeString(Json.stringify(config, "\t"));
					out.flush();
					Sys.sleep(config.givePointTime);
				}
			});
		}
		while (true) {
			var line = socket.input.readLine();
			Sys.stdout().writeString(line + "\n");
			if (line.startsWith("PING")) {
				var pong = "PONG" + line.substring(4);
				Sys.stdout().writeString(pong + "\n");
				socket.output.writeString(pong + "\r\n");
			} else {
				var index = line.indexOf("~");
				if (index != -1) {
					var command = line.substring(index + 1);
					if (command == "help") {
						var help = "PRIVMSG ";
						if (config.game.toLowerCase().startsWith("skyrim")) {
							help += "www.skyrimcommands.com";
						} else {
							help += "www.falloutcheats.com";
						}
						socket.output.writeString(help + "\r\n");
					} else {
						var user = line.substring(1, line.indexOf("!"));
						userCall(user, command);
					}
				}
			}
			Sys.stdout().flush();
			socket.output.flush();
		}
	}

	static function userCall(user:String, command:String) {
		var points = 0;
		if (config.users.exists(user)) {
			points = config.users[user];
		}
		var cost = config.defaultCost;
		for (key in config.commands.keys()) {
			if (command.startsWith(key)) {
				cost = config.commands[key];
				break;
			}
		}
		if (cost < 0) {
			socket.output.writeString("PRIVMSG That command is banned!\r\n");
		} else if (cost > points) {
			socket.output.writeString("PRIVMSG "+user+", you have "+points+" points, you need "+cost+" points. You get a point every "+config.givePointTime+" seconds.");
		} else {
			config.users[user] -= cost;
			call(command);
		}
	}

	static function call(command:String) {
		Sys.command("sse", [command]);
	}
}
