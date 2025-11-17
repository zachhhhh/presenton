import { getHeader, getHeaderForFormData } from "./header";
import { IconSearch, ImageGenerate, ImageSearch, PreviousGeneratedImagesResponse } from "./params";
import { ApiResponseHandler } from "./api-error-handler";
import { apiFetch } from "@/lib/api-client";

type Nullable<T> = {
  [K in keyof T]: T[K] | null | undefined;
};

const sanitizePayload = <T extends object>(payload: Nullable<T>): T => {
  const entries = Object.entries(payload).filter(([, value]) => value !== undefined && value !== null);
  return Object.fromEntries(entries) as T;
};

const handleApiRequest = async <T = any>(
  request: () => Promise<Response>,
  defaultErrorMessage: string
): Promise<T> => {
  try {
    const response = await request();
    return await ApiResponseHandler.handleResponse(response, defaultErrorMessage);
  } catch (error) {
    console.error(defaultErrorMessage, error);
    throw error;
  }
};

export class PresentationGenerationApi {
  static async uploadDoc(documents: File[]) {
    const formData = new FormData();

    documents.forEach((document) => {
      formData.append("files", document);
    });

    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/files/upload`, {
          method: "POST",
          headers: getHeaderForFormData(),
          body: formData,
        }),
      "Failed to upload documents"
    );
  }

  static async decomposeDocuments(documentKeys: string[]) {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/files/decompose`, {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
            file_paths: documentKeys,
          }),
        }),
      "Failed to decompose documents"
    );
  }
 
   static async createPresentation({
    content,
    n_slides,
    file_paths,
    language,
    tone,
    verbosity,
    instructions,
    include_table_of_contents,
    include_title_slide,
    web_search,
    
  }: {
    content: string;
    n_slides: number | null;
    file_paths?: string[];
    language: string | null;
    tone?: string | null;
    verbosity?: string | null;
    instructions?: string | null;
    include_table_of_contents?: boolean;
    include_title_slide?: boolean;
    web_search?: boolean;
  }) {
    const payload = sanitizePayload({
      content,
      n_slides,
      file_paths,
      language,
      tone,
      verbosity,
      instructions,
      include_table_of_contents,
      include_title_slide,
      web_search,
    });

    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/presentation/create`, {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(payload),
        }),
      "Failed to create presentation"
    );
  }

  static async editSlide(
    slide_id: string,
    prompt: string
  ) {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/slide/edit`, {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
            id: slide_id,
            prompt,
          }),
        }),
      "Failed to update slide"
    );
  }

  static async updatePresentationContent(body: any) {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/presentation/update`, {
          method: "PATCH",
          headers: getHeader(),
          body: JSON.stringify(body),
        }),
      "Failed to update presentation content"
    );
  }

  static async presentationPrepare(presentationData: any) {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/presentation/prepare`, {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
        }),
      "Failed to prepare presentation"
    );
  }
  
  // IMAGE AND ICON SEARCH
  
  
  static async generateImage(imageGenerate: ImageGenerate) {
    const params = new URLSearchParams({ prompt: imageGenerate.prompt });
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/images/generate?${params.toString()}`, {
          method: "GET",
          headers: getHeader(),
        }),
      "Failed to generate image"
    );
  }

  static getPreviousGeneratedImages = async (): Promise<PreviousGeneratedImagesResponse[]> => {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/images/generated`, {
          method: "GET",
          headers: getHeader(),
        }),
      "Failed to get previous generated images"
    );
  }
  
  static async searchIcons(iconSearch: IconSearch) {
    const params = new URLSearchParams({
      query: iconSearch.query,
      limit: String(iconSearch.limit),
    });

    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/icons/search?${params.toString()}`, {
          method: "GET",
          headers: getHeader(),
        }),
      "Failed to search icons"
    );
  }



  // EXPORT PRESENTATION
  static async exportAsPPTX(presentationData: any) {
    return handleApiRequest(
      () =>
        apiFetch(`/api/v1/ppt/presentation/export/pptx`, {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
        }),
      "Failed to export as PowerPoint"
    );
  }
  
  

}
