import argparse
import pathlib
import sys

from simple_pyyuque import SimplePyYuQueAPI


def main():
    parser = argparse.ArgumentParser(description="cmd arguments")
    parser.add_argument("--save_path", type=str, default="saved_files")
    parser.add_argument("--appname", type=str, default="test")
    parser.add_argument("--token", type=str, default="")
    parser.add_argument("--login", type=str, default="")

    args = parser.parse_args()
    save_dir = pathlib.Path("./") / args.save_path
    if args.token == "" or args.login == "":
        print("specify token first!!!")
        sys.exit(0)

    pysq = SimplePyYuQueAPI(token=args.token, app_name=args.app_name)
    user = pysq.User()
    user_serializer = user.get_users(login=args.login)
    print("recv user name: {}".format(user_serializer.name))
    print("Is it you? Input yes/no")
    verify = input()
    if verify.lower() != "yes":
        print("user incorrect")
        sys.exit(0)

    print("start downloading...")
    repo = pysq.Repo()
    ret = repo.get_users_repos(login=args.login)
    doc_api = pysq.Doc()
    for ns in ret.book_serializer_list:
        print("------------------------")
        print("------------------------")
        print("downloading book {}".format(ns.namespace))
        print("------------------------")
        print("------------------------")
        docs = doc_api.get_repos_docs(namespace=ns.namespace)
        for doc in docs.doc_serializer_list:
            doc_detail = doc_api.get_repos_docs_detail(
                namespace=ns.namespace, slug=doc.slug, repo_id=ns.id, id=doc.id
            )
            doc_title = doc_detail.title
            # remove invalid character
            doc_title = (
                doc_title.replace(" ", "_")
                .replace("\\", "_")
                .replace("/", "_")
                .replace("|", "")
            )
            doc_md = doc_detail.body
            parent_dir = save_dir / ns.name
            parent_dir.mkdir(exist_ok=True)
            doc_file = parent_dir / (doc_title + ".md")
            if doc_file.exists():
                continue
            print("------------------------")
            print("downloading doc {}".format(doc_title))
            print("------------------------")
            f = doc_file.open(mode="w", encoding="utf-8")
            f.write(doc_md)


if __name__ == "__main__":
    main()
