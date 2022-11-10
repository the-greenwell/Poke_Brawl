// // /* 
// // Recursive Sigma
// // Input: integer
// // Output: sum of integers from 1 to Input integer
// // */

// // const num1 = 5;
// // const expected1 = 15;
// // // Explanation: (1+2+3+4+5)

// // const num2 = 2.5;
// // const expected2 = 3;
// // // Explanation: (1+2)

// // const num3 = -1;
// // const expected3 = 0;

// // /**
// //  * Recursively sum the given int and every previous positive int.
// //  * - Time: O(?).
// //  * - Space: O(?).
// //  * @param {number} num
// //  * @returns {number}
// //  */
// // function recursiveSigma(num, i=1, add=0 ) {
// //     if(Math.floor(num) < i){
// //         return add
// //     }
// //     add += i
// //     return recursiveSigma(num, i+1, add)
// // }
// // console.log(recursiveSigma(num3))


// // const nums1 = [1, 2, 3];
// // const expected10 = 6;

// // const nums2 = [1];
// // const expected20 = 1;

// // const nums3 = [];
// // const expected30 = 0;

// // /**
// //  * Add params if needed for recursion
// //  * Recursively sums the given array.
// //  * - Time: O(?).
// //  * - Space: O(?).
// //  * @param {Array<number>} nums
// //  * @returns {number} The sum of the given nums.
// // //  */
// // // function sumArr(nums, i=0, add=0) {
// // //     if(nums.length <= i){
// // //         return add
// // //     }
// // //     add += nums[i]
// // //     return sumArr(nums, i+1, add)

// // // }
// // // console.log(sumArr(nums3))

// /* 
//   Recursively reverse a string
//   helpful methods:
//   str.slice(beginIndex, endIndex)
//   returns a new string from beginIndex to endIndex exclusive
// */

// const str1 = "abcpoaidhf";
// const expected1 = "cba";

// const str2 = "";
// const expected2 = "";

// /**
//  * Recursively reverses a string.
//  * - Time: O(?).
//  * - Space: O(?).
//  * @param {string} str
//  * @returns {string} The given str reversed.
//  */
// function reverseStr(str) {
//     if (str.length < 1){
//         return str;
//     }
//     return str.slice(-1) + reverseStr(str.slice(0, -1))
// }

// console.log(reverseStr(str1))
/**********************/


const num1 = 5;
const expected1 = 5;

const num2 = 10;
const expected2 = 1;

const num3 = 2598;
const expected3 = 7;
/**
 * Sums the given number's digits until the number becomes one digit.
 * @param {number} num The number to sum to one digit.
 * @returns {number} One digit.
 */
function sumToOneDigit(num) {
  if (num < 10 ){ return num }
  let sum =  (num % 10) + sumToOneDigit(((num - (num % 10)) / 10))
  if (sum % 10 !== 0){
    sum = sumToOneDigit(sum)
  }
  return sum
}

console.log(sumToOneDigit(num1))