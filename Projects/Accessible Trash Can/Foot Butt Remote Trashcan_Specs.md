Concept name

Foot Butt Remote Trashcan

Core idea

A trash can lid that can open or close from two inputs:

1\. Foot pedal — purely mechanical, familiar, no batteries needed for basic use.

2\. Button controls — one button on the lid and one wireless wall/desk button. Press once: open. Press again: close.

The trash can has three “ways in”:

Foot for hands-free use.

Lid button for nearby manual control.

Remote button for when the can is across the room, under a desk, near a bed, near a changing table, etc.

The machine, in human terms

Think of the lid as a small drawbridge.

The foot pedal is the old rope-and-lever system.

The button system is a tiny motorized hand that can lift or lower the bridge on command.

The wireless button is just a distant finger telling that hand what to do.

Main engineering parts

1\. The bin body

This can start as an existing foot-pedal trash can.

Important features:

Hinged lid

Foot pedal linkage

Enough space near the hinge or back wall to mount small electronics

Lid not too heavy

2\. The actuator

This is the part that physically opens and closes the lid.

Most likely prototype options:

Servo motor: simplest for small lids; rotates to set positions.

Linear actuator: stronger, more “push/pull,” but bulkier.

Gear motor + linkage: more custom, more robust later.

For prototype: servo motor is probably the cleanest first move.

3\. The control board

This is the little “nervous system.”

It listens for button presses and tells the motor what position to move to.

Good prototype options:

Arduino Nano

ESP32

Raspberry Pi Pico

For your use case: ESP32 may be ideal because it can handle wireless later, but Arduino Nano may feel simpler at first.

4\. The buttons

There are two electronic inputs:

Button on lid

Wireless button/transmitter

Both do the same thing:

\> “Change state.”

Meaning:

If lid is closed → open it.

If lid is open → close it.

This is called a toggle.

5\. The remote transmitter

This could be approached two ways:

Easiest prototype path:

Use an off-the-shelf wireless relay/button kit.

The remote button sends a signal to a receiver inside the trash can. The receiver acts like a button press.

Cleaner later-product path:

Custom RF or Bluetooth Low Energy button.

For now, don’t overbuild that part. The prototype only needs to prove the experience.

Control logic

In engineering terms, the system has two states:

\`\`\`text

STATE 1: Lid closed

STATE 2: Lid open

\`\`\`

And one command:

\`\`\`text

Toggle

\`\`\`

So the brain is simple:

\`\`\`text

When lid button is pressed:

if lid is closed, open lid

if lid is open, close lid

When remote button is pressed:

if lid is closed, open lid

if lid is open, close lid

\`\`\`

The “magic” is not the code.

The magic is that every input speaks the same language.

Prototype version 1

Goal

Make a trash can lid open/close by button.

Ignore wireless at first.

Build:

Existing foot-pedal trash can

Servo motor mounted near hinge

Arduino/ESP32

One button on lid

Battery pack or wall power

Simple linkage from servo arm to lid

Success condition:

\> Press button once, lid opens. Press again, lid closes.

That alone proves the core mechanism.

Prototype version 2

Add the remote.

Build:

Same system as version 1

Add wireless relay receiver

Add adhesive-backed remote button

The receiver should connect to the same place the lid button connects.

In plain terms:

\> The remote button pretends to be the lid button from far away.

That is probably the wiring piece you’re sensing as the hard part—but conceptually, it’s not two separate systems. It’s one button circuit with two possible button sources.

Prototype version 3

Make it feel like a product.

Add:

Better motor mount

Hidden wiring

Rechargeable battery

Quiet-close movement

Limit detection so the motor knows when the lid is fully open/closed

Manual override so foot pedal still works safely

Better casing for electronics

One important engineering concern

The foot pedal and motor need to coexist.

The motor should not fight the foot pedal.

So the linkage may need either:

A loose/slotted connection

A clutch-like joint

A spring-assisted hinge

Or motor actuation only on the lid, while pedal remains mechanically independent

That’s the main physical design puzzle.

Clean product sentence

A dual-control trash can that preserves the reliability of a foot pedal while adding button and wireless remote lid control for lower-friction use across domestic, accessibility, care, and workspace contexts.

The essence

This is not “a trash can with a button.”

It is:

\> A low-friction lid system with multiple human access points: foot, hand, and distance.