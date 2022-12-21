## radioLog

# Background
Shortwave radio waves have the unique characteristic that they can be propagated across the globe indirectly, thanks to refraction in the upper atmosphere. However, these connections can be somewhat sporadic, so much time is dedicated by ham radio enthusiasts to increasing reception and exploiting the refraction effects. The FT8 communication mode, a feature of the WSJT-X program, enables hams to send tiny messages in 15-second increments via shortwave radio.

I have set up a receiving station because I am curious about discovering which long-range stations I can listen in to. I use WSJT-X and I pipe it audio from SDR#, a program which can tune the RTL-SDR radio dongle. The RTL-SDR is a radio tuner that nerds have hacked to receive signal from many parts of the radio spectrum. It is an SDR (software-defined radio), and thus infinitely hackable. Using a few simple programs, then, I can listen in to hams from all around the world attempt to communicate to one another. I do this just because I find the technology and science of the topic interesting--for instance, antenna design is a huge part of the reception of these signals, another interest of mine.

# What is this?
Essentially, the WSJT-X program logs each signal that it receives to a file called ALL.TXT. All that I want is to be able to view which stations I've received. To do this, I'll simply place any WSJT-X file I want to log into /toBeProcessed and run `python processLogs.py`. From there... who knows? Maybe I'll figure out some pythonic way of mapping these--after all, the FT8 mode does force CQ'ers to give their approximate location on a global grid.

# How to run:
1. Insert a WSJT-X ALL.TXT file into "toBeProcessed"
2. `python processLogs.py`
