// blocks.js — defines the puzzle blocks and their shapes

const blocks = [
  // Volume 1
  { id: 1, name: "Block 01", color: "rgb(239, 139, 27)", volume: 1, shape: [[0, 0, 0]] },

  // Volume 2
  { id: 2, name: "Block 02", color: "rgb(106, 194, 84)", volume: 2, shape: [[0,0,0], [1,0,0]] },

  // Volume 3
  { id: 3, name: "Block 03", color: "rgb(244, 195, 203)", volume: 3, shape: [[0,0,0], [1,0,0], [2,0,0]] },
  { id: 4, name: "Block 04", color: "rgb(252, 221, 80)", volume: 3, shape: [[0,0,0], [0,1,0], [0,2,0]] },

  // Volume 4
  { id: 5, name: "Block 05", color: "purple-blue", volume: 4, shape: [[0,0,0], [1,0,0], [1,1,0], [2,1,0]] },
  { id: 6, name: "Block 06", color: "rgb(239, 139, 27)", volume: 4, shape: [[0,0,0], [1,0,0], [1,1,0], [1,2,0]] },
  { id: 7, name: "Block 07", color: "rgb(239, 139, 27)", volume: 4, shape: [[0,0,0], [0,1,0], [1,1,0], [1,2,0]] },
  { id: 8, name: "Block 08", color: "rgb(239, 139, 27)", volume: 4, shape: [[0,0,0], [0,1,0], [0,2,0], [1,0,0]] },
  { id: 9, name: "Block 09", color: "rgb(252, 221, 80)", volume: 4, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0]] },
  { id: 10, name: "Block 10", color: "rgb(244, 195, 203)", volume: 4, shape: [[0,0,0], [0,1,0], [0,2,0], [1,2,0]] },
  { id: 11, name: "Block 11", color: "rgb(239, 139, 27)", volume: 4, shape: [[0,0,0], [1,0,0], [1,1,0], [2,0,0]] },

  // Volume 5
  { id: 12, name: "Block 12", color: "rgb(106, 194, 84)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0], [2,2,0]] },
  { id: 13, name: "Block 13", color: "rgb(252, 221, 80)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0], [3,1,0]] },
  { id: 14, name: "Block 14", color: "rgb(239, 139, 27)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [1,1,0], [2,1,0]] },
  { id: 15, name: "Block 15", color: "rgb(252, 221, 80)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 16, name: "Block 16", color: "rgb(106, 194, 84)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 17, name: "Block 17", color: "rgb(106, 194, 84)", volume: 5, shape: [[0,0,0], [0,1,0], [0,2,0], [1,2,0], [2,2,0]] },
  { id: 18, name: "Block 18", color: "rgb(244, 195, 203)", volume: 5, shape: [[0,0,0], [0,1,0], [0,2,0], [1,1,0], [2,1,0]] },
  { id: 19, name: "Block 19", color: "rgb(244, 195, 203)", volume: 5, shape: [[0,0,0], [0,1,0], [0,2,0], [1,0,0], [2,0,0]] },
  { id: 20, name: "Block 20", color: "rgb(106, 194, 84)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 21, name: "Block 21", color: "rgb(106, 194, 84)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0], [2,2,0]] },
  { id: 22, name: "Block 22", color: "rgb(252, 221, 80)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 23, name: "Block 23", color: "rgb(239, 139, 27)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [1,1,0], [1,2,0]] },
  { id: 24, name: "Block 24", color: "rgb(252, 221, 80)", volume: 5, shape: [[0,0,0], [0,1,0], [0,2,0], [1,1,0], [2,1,0]] },
  { id: 25, name: "Block 25", color: "rgb(244, 195, 203)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 26, name: "Block 26", color: "rgb(244, 195, 203)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 27, name: "Block 27", color: "rgb(87, 194, 230)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0], [3,1,0]] },
  { id: 28, name: "Block 28", color: "rgb(167, 99, 137)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 29, name: "Block 29", color: "rgb(87, 194, 230)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 30, name: "Block 30", color: "rgb(167, 99, 137)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [1,1,0], [2,1,0]] },
  { id: 31, name: "Block 31", color: "rgb(87, 194, 230)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [1,2,0], [2,2,0]] },
  { id: 32, name: "Block 32", color: "rgb(167, 99, 137)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 33, name: "Block 33", color: "rgb(87, 194, 230)", volume: 5, shape: [[0,0,0], [1,0,0], [2,0,0], [2,1,0], [2,2,0]] },
  { id: 34, name: "Block 34", color: "rgb(167, 99, 137)", volume: 5, shape: [[0,0,0], [1,0,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 35, name: "Block 35", color: "rgb(87, 194, 230)", volume: 5, shape: [[0,0,0], [0,1,0], [1,1,0], [2,1,0], [2,2,0]] },
  { id: 36, name: "Block 36", color: "rgb(167, 99, 137)", volume: 5, shape: [[0,0,0], [0,1,0], [0,2,0], [1,2,0], [2,2,0]] },
];
