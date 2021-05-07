//array with keys pressed at the same time
let keys = [];

let prev_command;

const socket = new WebSocket("ws://localhost:3333");
const ORIGIN = "controller";

/**
 * below are constant objects containing info of all commands,
 * like the commands itself, it's keycode and the key(s) that needs to be pressed for the command
 */
const GO_FORWARDS = {
  name: "GO_FORWARDS",
  keycode: 87,
  key: "w",
};
const TURN_LEFT = {
  name: "TURN_LEFT",
  keycode: 65,
  key: "a",
};
const GO_BACKWARDS = {
  name: "GO_BACKWARDS",
  keycode: 83,
  key: "s",
};
const TURN_RIGHT = {
  name: "TURN_RIGHT",
  keycode: 68,
  key: "d",
};
const FORWARD_TURN_LEFT = {
  name: "FORWARD_TURN_LEFT",
  keycode: [65, 87],
  key: "a+w",
};
const FORWARD_TURN_RIGHT = {
  name: "FORWARD_TURN_RIGHT",
  keycode: [68, 87],
  key: "d+w",
};
const BACKWARD_TURN_RIGHT = {
  name: "BACKWARD_TURN_RIGHT",
  keycode: [65, 83],
  key: "a+s",
};
const BACKWARD_TURN_LEFT = {
  name: "BACKWARD_TURN_LEFT",
  keycode: [68, 83],
  key: "d+s",
};
const ONE_KEY_COMMANDS = [
  GO_FORWARDS,
  TURN_LEFT,
  GO_BACKWARDS,
  TURN_RIGHT,
];
const MULTIPLE_KEY_COMMANDS = [
  FORWARD_TURN_LEFT,
  FORWARD_TURN_RIGHT,
  BACKWARD_TURN_RIGHT,
  BACKWARD_TURN_LEFT,
];

/**
 * keydown and keyup eventlistener, looks at keys that are pressed and compares them to all commands.
 * if a command is found, it sends this command to the socketserver, which will send it to the simulation
 * if a command is not found, it sends the command "NONE"
 **/
window.addEventListener("keydown", function (event) {
  if (keys.includes(event.keyCode)) {
    return;
  }
  keys.push(event.keyCode);
  document.getElementById("keycode_pressed").innerHTML = keys;
  if (keys.length < 2) {
    for (let i = 0; i < ONE_KEY_COMMANDS.length; i++) {
      if (ONE_KEY_COMMANDS[i].keycode == keys) {
        document.getElementById("key_pressed").innerHTML =
          ONE_KEY_COMMANDS[i].name;
        send(ONE_KEY_COMMANDS[i].name);
        console.log(ONE_KEY_COMMANDS[i].name);
        break;
      }
    }
  } else {
    let command = "NONE";
    for (let i = 0; i < MULTIPLE_KEY_COMMANDS.length; i++) {
      if (keys.length == MULTIPLE_KEY_COMMANDS[i].keycode.length) {
        keys.sort();
        MULTIPLE_KEY_COMMANDS[i].keycode.sort();
        if (
          JSON.stringify(MULTIPLE_KEY_COMMANDS[i].keycode) ===
          JSON.stringify(keys)
        ) {
          command = MULTIPLE_KEY_COMMANDS[i].name;
          break;
        }
      }
    }
    document.getElementById("key_pressed").innerHTML = command;
    send(command);
    console.log(command);
  }
});
window.addEventListener("keyup", function (event) {
  keys.splice(keys.indexOf(event.keyCode), 1);
  document.getElementById("keycode_pressed").innerHTML = keys;
  if (keys.length < 2) {
    for (let i = 0; i < ONE_KEY_COMMANDS.length; i++) {
      if (ONE_KEY_COMMANDS[i].keycode == keys) {
        document.getElementById("key_pressed").innerHTML =
          ONE_KEY_COMMANDS[i].name;
        send(ONE_KEY_COMMANDS[i].name);
        console.log(ONE_KEY_COMMANDS[i].name);
        break;
      }
    }
  } else {
    let command = "NONE";
    for (let i = 0; i < MULTIPLE_KEY_COMMANDS.length; i++) {
      if (keys.length == MULTIPLE_KEY_COMMANDS[i].keycode.length) {
        keys.sort();
        MULTIPLE_KEY_COMMANDS[i].keycode.sort();
        if (
          JSON.stringify(MULTIPLE_KEY_COMMANDS[i].keycode) ===
          JSON.stringify(keys)
        ) {
          command = MULTIPLE_KEY_COMMANDS[i].name;
          break;
        }
      }
    }
    document.getElementById("key_pressed").innerHTML = command;
    send(command);
    console.log(command);
  }
  if (keys.length === 0) {
    document.getElementById("key_pressed").innerHTML = "NONE";
    send("NONE");
    console.log("NONE");
  }
});

/**
 * prevents sending a command multiple times,
 * also sends the command to the socket server
 * @param {string} command
 */
function send(command) {
  if (prev_command == command) {
    return;
  }
  prev_command = command;
  socket.send(command);
}
/**
 * lists all possible commands with the keys that need to be pressed to use them
 */
function listcommands() {
  for (let i = 0; i < ONE_KEY_COMMANDS.length; i++) {
    var li = document.createElement("li");
    li.appendChild(
      document.createTextNode(
        ONE_KEY_COMMANDS[i].key + " " + ONE_KEY_COMMANDS[i].name
      )
    );
    li.id = "command";
    document.getElementById("possible_one_key_commands").appendChild(li);
  }
  for (let i = 0; i < MULTIPLE_KEY_COMMANDS.length; i++) {
    var li = document.createElement("li");
    li.appendChild(
      document.createTextNode(
        MULTIPLE_KEY_COMMANDS[i].key + " " + MULTIPLE_KEY_COMMANDS[i].name
      )
    );
    li.id = "command";
    document.getElementById("possible_multiple_key_commands").appendChild(li);
  }
}
//fixme, find a better place
listcommands();
