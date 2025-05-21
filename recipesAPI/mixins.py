class AdminApprovalMixin:
    def perform_approval_logic(self, instance, serializer, user):
        current_status = getattr(instance, 'admin_approved')
        new_status = serializer.validated_data.get(
            'admin_approved', current_status)

        if current_status != new_status:
            if new_status == True:
                return serializer.save(approved_by=user)
            else:
                return serializer.save(approved_by=None)
        else:
            return serializer.save()
