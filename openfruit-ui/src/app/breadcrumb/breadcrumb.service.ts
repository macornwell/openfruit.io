
class BreadcrumbNode {
  constructor(
    private text: string,
    private url: string) {
  }
}

export class BreadCrumbService {
  private nodes: BreadcrumbNode[] = [];

  reset() {
    this.nodes = [];
  }

  addNode(text: string, url: string) {
    this.nodes.push(new BreadcrumbNode(text, url));
  }

  getNodes() {
    return this.nodes;
  }

  hasNodes() {
    return this.nodes.length > 0;
  }
}
