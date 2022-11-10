// const num1 = 3;
// const expected1 = 6;
// // Explanation: 1*2*3 = 6

// const num2 = 6.8;
// const expected2 = 720;
// // Explanation: 1*2*3*4*5*6 = 720

// const num3 = 0;
// const expected3 = 1;

// /**
//  * Recursively multiples 1 to the given int.
//  * - Time: O(?).
//  * - Space: O(?).
//  * @param {number} n The int to factorial. Treat negatives as zero and
//  *    floor decimals.
//  * @returns {number} The result of !n.
//  */
// function factorial(n) {
//     if (Math.floor(n) <= 1){
//         return 1
//     }
//     return Math.floor(n) * factorial(n-1)
// }
// console.log(factorial(num3))

/* 
    Return the fibonacci number at the nth position, recursively.
    
    Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    The next number is found by adding up the two numbers before it,
    starting with 0 and 1 as the first two numbers of the sequence.
*/



const num1 = 0;
const expected1 = 0;

const num2 = 1;
const expected2 = 1;

const num3 = 2;
const expected3 = 1;

const num4 = 3;
const expected4 = 2;

const num5 = 4;
const expected5 = 3;

const num6 = 8;
const expected6 = 21;

/**
 * Recursively finds the nth number in the fibonacci sequence.
 * - Time: O(?).
 * - Space: O(?).
 * @param {number} num The position of the desired number in the fibonacci sequence.
 * @returns {number} The fibonacci number at the given position.
 */
function fibonacci(num, i = 1, start = 1, prev = 0) {
    return num < i ? prev : fibonacci(num, i + 1, start + prev, prev = start)
}

console.log(fibonacci(num6))

// function fibonacci(num, i = 1, start = 1, prev = 0) {
//     if(num < i){
//         return prev
//     }
//     return fibonacci(num, i + 1, start + prev, prev = start)
// }