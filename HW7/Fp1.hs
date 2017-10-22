head' :: [a] -> a
head' (x:_) = x

tail' :: [a] -> [a]
tail' (_:x) = x

take' :: Int -> [a] -> [a]
take' n (x:l) = if n == 0
				then []
				else x : take' (n - 1) l 

drop' :: Int -> [a] -> [a]
drop' n (x:l)
	| n == 0 = x : l
	| null l = []
	| otherwise = drop' (n - 1) l

filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs
	| null xs = []
	| f (head' xs) = (head' xs) : (filter' f (tail' xs))
	| otherwise = filter' f (tail' xs)


foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z l = if null l
				then z
				else foldl' f (f z (head' l)) (tail' l)

concat' :: [a] -> [a] -> [a]
concat' fl sl = if null fl
				then sl
				else (head' fl) : (concat' (tail' fl) sl)

length' :: [a] -> Int
length' xs
 	| null xs = 0
 	| otherwise = 1 + length' (tail' xs)

--pivot' xs = head' xs
pivot' xs = head' (drop' ((length' xs) `div` 2) xs)
--partition mid xs = ( (filter' (<= mid) xs ) (filter' (> mid) xs) )

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' xs = concat' (concat' (quickSort'(filter' (< (pivot' xs)) xs)) (filter' (== (pivot' xs)) xs)) (quickSort'(filter' (> (pivot' xs)) xs))