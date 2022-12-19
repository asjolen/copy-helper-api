from utils.user.user_helper import UserHelper
from team.models import Member as TeamMember
from organization.models import Member as OrganizationMember


class IsOrganizationAndTeamMember:
    """ Check if user is member of team """
    user_helper = UserHelper()

    def has_permission(self, request, view):
        organization = self.user_helper.get_current_organization(request)
        team = self.user_helper.get_current_team(request)
        user = self.user_helper.authenticated_user(request)

        # Check access
        query_organization_member = OrganizationMember.objects.filter(user=user, organization=organization).first()
        query_team_member = TeamMember.objects.filter(user=user, team=team).first()

        if query_organization_member and query_team_member:
            return True

        return False


class IsOrganizationManager:
    user_helper = UserHelper()

    def has_permission(self, request, view):
        organization = self.user_helper.get_current_organization(request)
        user = self.user_helper.authenticated_user(request)

        # Check access
        query_organization_member = OrganizationMember.objects.filter(user=user, organization=organization).first()

        if query_organization_member and query_organization_member.role == self.user_helper.ORGANIZATION_MANAGER:
            return True

        return False


class IsTeamManager:
    user_helper = UserHelper()

    def has_permission(self, request, view):
        team = self.user_helper.get_current_team(request)
        user = self.user_helper.authenticated_user(request)

        # Check access
        query_team_member = TeamMember.objects.filter(user=user, team=team).first()

        if query_team_member and query_team_member.role == self.user_helper.TEAM_MANAGER:
            return True

        return False