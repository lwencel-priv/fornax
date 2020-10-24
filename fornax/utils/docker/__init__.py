class Docker:
    @staticmethod
    def build_cmd(dockerfile_path: str, image_name: str) -> list:
        """[summary].

        :param dockerfile_path: [description]
        :type dockerfile_path: str
        :param image_name: [description]
        :type image_name: str
        :return: [description]
        :rtype: [type]
        """
        return ["docker", "build", "-f", dockerfile_path, "-t", image_name]
