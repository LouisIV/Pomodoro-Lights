# Pomodoro Lights
I'm someone who loves the idea of Pomodoro clocks. I say the idea because I can never seem to hold myself to actually take a break when the alarm goes off. Having tried almost every app in the App Store I realized it would be great if I could just make it impossible for me to ignore the timer. Maybe by turning the lights off?

After cloning the project you will need to setup a configuration file like this
```
~/.config/pomoli/pomoli.json
```

The file itself should look something like this
```
{
  "times" : {
  
    you can use anything for these values
    specify a duration with a number.
     
    "work" : 2,
    "short_break" : 5,
    "long_break" : 45
  },
  "cycle" : [
  
    Next you need to tell the program what
    order you want everything to happen in.
    
    "work", "short_break",
    "work", "short_break",
    "long_break"
  ],
}
```
For a basic configuration that's all you need but if you want to use some of the other features you'll need to add a few more entries.
```
"effects" : {

  Here you define the effects on a value by value basis.
  
  "work" : {
    
    Next you define which service you want to leave instructions for.
    Currently the only working interaction is Yeelight.
    
    "yeelight" : [
      {
        "type": "steady",
        "color": "36ed36"
      },
      {
        "type": "pulse",
        "color": "ed3636",
        "pulses": 2
      }
    ]
  }
}
```
Then you also need to define settings for some of the services.
```
"yeelight_settings" : [
  {
    "ip": "192.168.86.133",
    "name" : "Light Name",
    "group" : "Light Group",
    "type": "strip"
  }
]
```
