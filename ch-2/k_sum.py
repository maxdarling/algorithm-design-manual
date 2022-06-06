def kSumOpt(self, nums, target, k):
        '''
        Return a list of all unique k-lists l = [nums[i_1], ..., nums[i_k]] 
        for which sum(l) = target

        Recursive solution: O(n^(k-1)) (optimal)

        kSum(nums, target, k) = 
          [[a] + l | a in nums, l in kSum(nums - [a], target - a, k-1)]

        kSum(nums, target, 2) = twoSum(nums, target)
        
        Optimization using ranges:
        notice for k sum with range start param,
        f(k, start=0) = first elem n[0] with f(k - 1, 1) + 
                  first elem n[1] with f(k-1, 2) + 
                  ... + 
                  first elem n[n-k] with f(k-1, n-k+1)
                  
        Why? Well, one way to think about it is: 
        Assume you're computing f(k, i) (as above). You say in order to
        complete some k-list, you need an element at idx j before your start
        idx i. I claim you never do, because f(k, j) would have covered it!
        '''
        # sort nums
        nums.sort()

        # recursive helper. uses ranges to prevent dupes, instead of map of counts
        def r(target, k, start):
            if (start > len(nums) - k): # early termination
                return []
            
            # todo: optimization - check first and last elems against target / k
            
            if (k == 2): # base case
                return self.twoSum(nums, target, start)

            result = set()
            used_starting_nums = set()

            for i in range(start, len(nums)):
                if nums[i] in used_starting_nums: 
                    # optimization - skip dupe starting nums.
                    # first usage will have a larger range than all future usages,
                    # and therefore is a superset / covers all they might contribute
                    continue
                for tup in r(target - nums[i], k - 1, i + 1):
                    k_tup = tuple(sorted([nums[i]] + list(tup)))
                    result.add(k_tup)
                    
                used_starting_nums.add(nums[i])

            return result

        return r(target, k, 0)


def twoSum(self, nums, target, start = 0):
        '''
        Return list of all unique pairs [nums[i], nums[j]] for which
        nums[i] + nums[j] = target

        "2 pointer" method - assumes nums sorted in increasing order
        '''

        # lo and hi ptr
        lo = start
        hi = len(nums) - 1
        result = []

        # alg: move pointers inward to find pairs
        while (lo < hi):
            pair_sum = nums[lo] + nums[hi]
            if (pair_sum == target):
                result.append([nums[lo], nums[hi]])
                # skip all dupes
                while True:
                    lo += 1
                    if not (lo < hi and nums[lo - 1] == nums[lo]):
                        break
                while True:
                    hi -= 1
                    if not (hi >= lo and nums[hi] == nums[hi + 1]):
                        break

            elif (pair_sum < target):
                lo += 1
            else:
                hi -= 1

        return result
