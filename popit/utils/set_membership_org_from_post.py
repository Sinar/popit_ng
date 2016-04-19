from popit.models import Membership

def main():
    memberships = Membership.objects.language("en").all()
    for membership in memberships:
        if not membership.organization:
            if membership.post:
                if membership.post.organization:
                    membership.organization = membership.post.organization
        membership.save()

if __name__ == "__main__":
    main()