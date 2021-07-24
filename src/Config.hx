typedef Config = {
    ssl:Bool,
    host:String,
    port:Int,
    game:String,
    pass:String,
    user:String,
    channel:String,
    givePointTime:Int,
    commands:Map<String, Int>,
    users:Map<String, Int>
}