// @ts-nocheck -- skip type checking
import { _runtime } from "fumadocs-mdx/runtime/next"
import _source from "../source.config"

export const map = _runtime.docs(_source.docs || [], _source.meta || []).toFumadocsSource()
