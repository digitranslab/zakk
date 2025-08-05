import {
  AxeroIcon,
  BookstackIcon,
  ClickupIcon,
  ConfluenceIcon,
  DiscourseIcon,
  Document360Icon,
  DropboxIcon,
  GithubIcon,
  GitlabIcon,
  GlobeIcon,
  GmailIcon,
  GongIcon,
  GoogleDriveIcon,
  GoogleSitesIcon,
  GuruIcon,
  HubSpotIcon,
  JiraIcon,
  LinearIcon,
  LoopioIcon,
  NotionIcon,
  ProductboardIcon,
  R2Icon,
  SalesforceIcon,
  SharepointIcon,
  TeamsIcon,
  SlabIcon,
  ZendeskIcon,
  ZulipIcon,
  MediaWikiIcon,
  WikipediaIcon,
  AsanaIcon,
  S3Icon,
  OCIStorageIcon,
  GoogleStorageIcon,
  ColorSlackIcon,
  XenforoIcon,
  ColorDiscordIcon,
  FreshdeskIcon,
  FirefliesIcon,
  EgnyteIcon,
  AirtableIcon,
  GlobeIcon2,
  FileIcon2,
  GitbookIcon,
  HighspotIcon,
  EmailIcon,
} from "@/components/icons/icons";
import { ValidSources } from "./types";
import { SourceCategory, SourceMetadata } from "./search/interfaces";
import { Persona } from "@/app/admin/assistants/interfaces";

interface PartialSourceMetadata {
  icon: React.FC<{ size?: number; className?: string }>;
  displayName: string;
  category: SourceCategory;
  docs?: string;
  oauthSupported?: boolean;
  federated?: boolean;
  federatedTooltip?: string;
  // federated connectors store the base source type if it's a source
  // that has both indexed connectors and federated connectors
  baseSourceType?: ValidSources;
}

type SourceMap = {
  [K in ValidSources | "federated_slack"]: PartialSourceMetadata;
};

const slackMetadata = {
  icon: ColorSlackIcon,
  displayName: "Slack",
  category: SourceCategory.Messaging,
  docs: "https://docs.digi-trans.org/connectors/slack",
  oauthSupported: true,
  federated: true,
  federatedTooltip:
    "⚠️ WARNING: Due to Slack's rate limit and ToS changes, Slack is now federated. " +
    "This will result in significantly greater latency and lower search quality.",
  baseSourceType: "slack",
};

export const SOURCE_METADATA_MAP: SourceMap = {
  web: {
    icon: GlobeIcon2,
    displayName: "Web",
    category: SourceCategory.Other,
    docs: "https://docs.digi-trans.org/connectors/web",
  },
  file: {
    icon: FileIcon2,
    displayName: "File",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/file",
  },
  slack: slackMetadata,
  federated_slack: slackMetadata,
  discord: {
    icon: ColorDiscordIcon,
    displayName: "Discord",
    category: SourceCategory.Messaging,
    docs: "https://docs.digi-trans.org/connectors/discord",
  },
  gmail: {
    icon: GmailIcon,
    displayName: "Gmail",
    category: SourceCategory.Messaging,
    docs: "https://docs.digi-trans.org/connectors/gmail/overview",
  },
  google_drive: {
    icon: GoogleDriveIcon,
    displayName: "Google Drive",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/google_drive/overview",
    oauthSupported: true,
  },
  github: {
    icon: GithubIcon,
    displayName: "Github",
    category: SourceCategory.CodeRepository,
    docs: "https://docs.digi-trans.org/connectors/github",
  },
  gitlab: {
    icon: GitlabIcon,
    displayName: "Gitlab",
    category: SourceCategory.CodeRepository,
    docs: "https://docs.digi-trans.org/connectors/gitlab",
  },
  confluence: {
    icon: ConfluenceIcon,
    displayName: "Confluence",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/confluence",
    oauthSupported: true,
  },
  jira: {
    icon: JiraIcon,
    displayName: "Jira",
    category: SourceCategory.ProjectManagement,
    docs: "https://docs.digi-trans.org/connectors/jira",
  },
  notion: {
    icon: NotionIcon,
    displayName: "Notion",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/notion",
  },
  zendesk: {
    icon: ZendeskIcon,
    displayName: "Zendesk",
    category: SourceCategory.CustomerSupport,
    docs: "https://docs.digi-trans.org/connectors/zendesk",
  },
  gong: {
    icon: GongIcon,
    displayName: "Gong",
    category: SourceCategory.Other,
    docs: "https://docs.digi-trans.org/connectors/gong",
  },
  linear: {
    icon: LinearIcon,
    displayName: "Linear",
    category: SourceCategory.ProjectManagement,
    docs: "https://docs.digi-trans.org/connectors/linear",
  },
  productboard: {
    icon: ProductboardIcon,
    displayName: "Productboard",
    category: SourceCategory.ProjectManagement,
    docs: "https://docs.digi-trans.org/connectors/productboard",
  },
  slab: {
    icon: SlabIcon,
    displayName: "Slab",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/slab",
  },
  zulip: {
    icon: ZulipIcon,
    displayName: "Zulip",
    category: SourceCategory.Messaging,
    docs: "https://docs.digi-trans.org/connectors/zulip",
  },
  guru: {
    icon: GuruIcon,
    displayName: "Guru",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/guru",
  },
  hubspot: {
    icon: HubSpotIcon,
    displayName: "HubSpot",
    category: SourceCategory.CustomerRelationshipManagement,
    docs: "https://docs.digi-trans.org/connectors/hubspot",
  },
  document360: {
    icon: Document360Icon,
    displayName: "Document360",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/document360",
  },
  bookstack: {
    icon: BookstackIcon,
    displayName: "BookStack",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/bookstack",
  },
  google_sites: {
    icon: GoogleSitesIcon,
    displayName: "Google Sites",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/google_sites",
  },
  loopio: {
    icon: LoopioIcon,
    displayName: "Loopio",
    category: SourceCategory.Other,
  },
  dropbox: {
    icon: DropboxIcon,
    displayName: "Dropbox",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/dropbox",
  },
  salesforce: {
    icon: SalesforceIcon,
    displayName: "Salesforce",
    category: SourceCategory.CustomerRelationshipManagement,
    docs: "https://docs.digi-trans.org/connectors/salesforce",
  },
  sharepoint: {
    icon: SharepointIcon,
    displayName: "Sharepoint",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/sharepoint",
  },
  teams: {
    icon: TeamsIcon,
    displayName: "Teams",
    category: SourceCategory.Messaging,
    docs: "https://docs.digi-trans.org/connectors/teams",
  },
  discourse: {
    icon: DiscourseIcon,
    displayName: "Discourse",
    category: SourceCategory.Messaging,
    docs: "https://docs.digi-trans.org/connectors/discourse",
  },
  axero: {
    icon: AxeroIcon,
    displayName: "Axero",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/axero",
  },
  wikipedia: {
    icon: WikipediaIcon,
    displayName: "Wikipedia",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/wikipedia",
  },
  asana: {
    icon: AsanaIcon,
    displayName: "Asana",
    category: SourceCategory.ProjectManagement,
    docs: "https://docs.digi-trans.org/connectors/asana",
  },
  mediawiki: {
    icon: MediaWikiIcon,
    displayName: "MediaWiki",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/mediawiki",
  },
  clickup: {
    icon: ClickupIcon,
    displayName: "Clickup",
    category: SourceCategory.ProjectManagement,
    docs: "https://docs.digi-trans.org/connectors/clickup",
  },
  s3: {
    icon: S3Icon,
    displayName: "S3",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/s3",
  },
  r2: {
    icon: R2Icon,
    displayName: "R2",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/r2",
  },
  oci_storage: {
    icon: OCIStorageIcon,
    displayName: "Oracle Storage",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/oci_storage",
  },
  google_cloud_storage: {
    icon: GoogleStorageIcon,
    displayName: "Google Storage",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/google_storage",
  },
  xenforo: {
    icon: XenforoIcon,
    displayName: "Xenforo",
    category: SourceCategory.Messaging,
  },
  ingestion_api: {
    icon: GlobeIcon,
    displayName: "Ingestion",
    category: SourceCategory.Other,
  },
  freshdesk: {
    icon: FreshdeskIcon,
    displayName: "Freshdesk",
    category: SourceCategory.CustomerSupport,
    docs: "https://docs.digi-trans.org/connectors/freshdesk",
  },
  fireflies: {
    icon: FirefliesIcon,
    displayName: "Fireflies",
    category: SourceCategory.Other,
    docs: "https://docs.digi-trans.org/connectors/fireflies",
  },
  egnyte: {
    icon: EgnyteIcon,
    displayName: "Egnyte",
    category: SourceCategory.Storage,
    docs: "https://docs.digi-trans.org/connectors/egnyte",
  },
  airtable: {
    icon: AirtableIcon,
    displayName: "Airtable",
    category: SourceCategory.Other,
    docs: "https://docs.digi-trans.org/connectors/airtable",
  },
  gitbook: {
    icon: GitbookIcon,
    displayName: "GitBook",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/gitbook",
  },
  highspot: {
    icon: HighspotIcon,
    displayName: "Highspot",
    category: SourceCategory.Wiki,
    docs: "https://docs.digi-trans.org/connectors/highspot",
  },
  imap: {
    icon: EmailIcon,
    displayName: "Email",
    category: SourceCategory.Messaging,
  },
  // currently used for the Internet Search tool docs, which is why
  // a globe is used
  not_applicable: {
    icon: GlobeIcon,
    displayName: "Not Applicable",
    category: SourceCategory.Other,
  },

  // Just so integration tests don't crash the UI
  mock_connector: {
    icon: GlobeIcon,
    displayName: "Mock Connector",
    category: SourceCategory.Other,
  },
} as SourceMap;

function fillSourceMetadata(
  partialMetadata: PartialSourceMetadata,
  internalName: ValidSources
): SourceMetadata {
  return {
    internalName: partialMetadata.baseSourceType || internalName,
    ...partialMetadata,
    adminUrl: `/admin/connectors/${internalName}`,
  };
}

export function getSourceMetadata(sourceType: ValidSources): SourceMetadata {
  const response = fillSourceMetadata(
    SOURCE_METADATA_MAP[sourceType],
    sourceType
  );

  return response;
}

export function listSourceMetadata(): SourceMetadata[] {
  /* This gives back all the viewable / common sources, primarily for
  display in the Add Connector page */
  const entries = Object.entries(SOURCE_METADATA_MAP)
    .filter(
      ([source, _]) =>
        source !== "not_applicable" &&
        source !== "ingestion_api" &&
        source !== "mock_connector" &&
        // use the "regular" slack connector when listing
        source !== "federated_slack"
    )
    .map(([source, metadata]) => {
      return fillSourceMetadata(metadata, source as ValidSources);
    });
  return entries;
}

export function getSourceDocLink(sourceType: ValidSources): string | null {
  return SOURCE_METADATA_MAP[sourceType].docs || null;
}

export const isValidSource = (sourceType: string) => {
  return Object.keys(SOURCE_METADATA_MAP).includes(sourceType);
};

export function getSourceDisplayName(sourceType: ValidSources): string | null {
  return getSourceMetadata(sourceType).displayName;
}

export function getSourceMetadataForSources(sources: ValidSources[]) {
  return sources.map((source) => getSourceMetadata(source));
}

export function getSourcesForPersona(persona: Persona): ValidSources[] {
  const personaSources: ValidSources[] = [];
  persona.document_sets.forEach((documentSet) => {
    documentSet.cc_pair_summaries.forEach((ccPair) => {
      if (!personaSources.includes(ccPair.source)) {
        personaSources.push(ccPair.source);
      }
    });
  });
  return personaSources;
}

export async function fetchTitleFromUrl(url: string): Promise<string | null> {
  try {
    const response = await fetch(url, {
      method: "GET",
      // If the remote site has no CORS header, this may fail in the browser
      mode: "cors",
    });
    if (!response.ok) {
      // Non-200 response, treat as a failure
      return null;
    }
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");
    // If the site has <title>My Demo Page</title>, we retrieve "My Demo Page"
    const pageTitle = doc.querySelector("title")?.innerText.trim() ?? null;
    return pageTitle;
  } catch (error) {
    console.error("Error fetching page title:", error);
    return null;
  }
}
