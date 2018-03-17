from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
	messsage = "You are not owner of this post"
	my_safe_method = ['GET','PUT']
	def has_permission(self,request,view):
		if request.method in self.my_safe_method:
			return True
		return False

	def has_object_permission(self,request,view,obj):
		
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user
