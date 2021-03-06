import Prelude hiding (lookup)


data BinaryTree k v = Nil
	| Node k v (BinaryTree k v) (BinaryTree k v)
	deriving (Show, Eq, Ord)


lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k Nil = Nothing
lookup k (Node key value nodel noder)
	| key == k = Just value
	| key < k = lookup k nodel
	| otherwise = lookup k noder


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil
insert k v (Node key value nodel noder)
	| key == k = Node key v nodel noder
	| key < k = Node key value (insert k v nodel) noder
	| otherwise = Node key value nodel (insert k v noder)


getMinKey (Node key value Nil _) = (key, value);
getMinKey (Node _ _ nodel _ ) = getMinKey nodel; 

merge Nil Nil = Nil
merge Nil noder = noder
merge nodel Nil = nodel
merge nodel noder = Node keyMin valueMin nodel $ delete keyMin noder
		where
			(keyMin, valueMin) = getMinKey noder;


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Node key value nodel noder)
	| key == k = merge nodel noder
	| key < k = Node key value (delete k nodel) noder
	| otherwise = Node key value nodel (delete k noder)
