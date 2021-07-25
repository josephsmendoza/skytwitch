class Config {
    // use ssl to connect
    public var ssl=false;
    // hostname to connect to
    public var host="irc.chat.twitch.tv";
    // port to connect to
    public var port=6667;
    // game to send commands to
    public var game="Skyrim";
    // auth token
    public var pass="oath:token";
    // bot username
    public var user="username";
    // channel to monitor
    public var channel="username";
    // time in seconds to give a point
    public var givePointTime=0;
    // list of commands and their costs
    public var commands= new Map<String, Int>();
    // list of users and their points
    public var users=new Map<String, Int>();
    // default command cost
    public var defaultCost=0;
    public function new() {
        //why
    }
}