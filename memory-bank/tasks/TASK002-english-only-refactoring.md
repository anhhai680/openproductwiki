# [TASK002] - Convert Project to English-Only Support

**Status:** Pending  
**Added:** 2025-01-28  
**Updated:** 2025-01-28

## Original Request
Analyze the #codebase then create task to update this wiki just supports English only. Else languages should remove out of project.

## Thought Process
After analyzing the codebase, I found that OpenProductWiki has extensive internationalization (i18n) support with the following components:

### Current Multi-Language Implementation:
1. **Frontend i18n Infrastructure:**
   - `src/i18n.ts` defines 7 supported locales: ['en', 'ja', 'zh', 'es', 'kr', 'vi', 'pt-br']
   - `src/messages/` folder contains 10 translation files: en.json, es.json, fr.json, ja.json, kr.json, pt-br.json, ru.json, vi.json, zh-tw.json, zh.json
   - `src/contexts/LanguageContext.tsx` provides language switching context (203 lines)
   - Language selection dropdown in `ConfigurationModal.tsx`
   - Browser language auto-detection functionality

2. **Backend Language Support:**
   - `api/config/lang.json` defines 10 supported languages
   - `api/websocket_wiki.py` handles language parameter and applies it to AI prompts
   - `api/rag.py` supports language parameter for retrieval
   - API endpoint `/lang/config` serves language configuration

3. **UI/UX Elements:**
   - Japanese-specific fonts (Noto_Sans_JP, Noto_Serif_JP) in layout.tsx
   - Language selection dropdown in configuration modal
   - Language persistence in localStorage
   - Language synchronization across components

### Strategy for English-Only Conversion:
The conversion should be done systematically to maintain code quality while removing all internationalization infrastructure. This involves:
1. Removing translation files and i18n configuration
2. Replacing dynamic translation strings with static English text
3. Removing language selection UI components
4. Simplifying backend language handling
5. Cleaning up font configurations
6. Updating documentation and configuration

This is a significant refactoring that will simplify the codebase and reduce maintenance overhead while maintaining all core functionality.

## Implementation Plan

### Phase 1: Backend Language Removal
- Remove `api/config/lang.json`
- Update `api/websocket_wiki.py` to remove language parameter handling
- Update `api/rag.py` to remove language parameter
- Remove `/lang/config` API endpoint
- Update AI prompts to remove language-specific instructions

### Phase 2: Frontend Translation Infrastructure Removal
- Remove `src/i18n.ts`
- Delete entire `src/messages/` directory and all translation files
- Remove `src/contexts/LanguageContext.tsx`
- Update components to remove `useLanguage` imports and usage

### Phase 3: Component Updates
- Update all components that use translation strings (t.xxx) to use static English text
- Remove language selection dropdown from ConfigurationModal
- Remove language-related state management from pages
- Remove language parameter from API calls

### Phase 4: Layout and Styling Cleanup
- Remove Japanese fonts from layout.tsx
- Update font configurations to use standard fonts
- Remove language-specific CSS classes

### Phase 5: Configuration and Documentation Updates
- Update next.config.ts to remove language routing
- Remove language-related environment variables or configuration
- Update README.md and documentation to reflect English-only support
- Clean up any remaining language-related code

## Progress Tracking

**Overall Status:** Not Started - 0%

### Subtasks
| ID | Description | Status | Updated | Notes |
|----|-------------|--------|---------|-------|
| 2.1 | Remove backend language configuration and API endpoints | Not Started | - | Remove lang.json, update websocket_wiki.py, rag.py, api.py |
| 2.2 | Delete frontend i18n infrastructure | Not Started | - | Remove i18n.ts, messages/ folder, LanguageContext.tsx |
| 2.3 | Update ConfigurationModal component | Not Started | - | Remove language dropdown and related functionality |
| 2.4 | Update main pages (home, repo pages) | Not Started | - | Replace translation calls with static English text |
| 2.5 | Update remaining components | Not Started | - | Ask, ModelSelectionModal, TokenInput, WikiTypeSelector, UserSelector |
| 2.6 | Clean up layout and font configurations | Not Started | - | Remove Japanese fonts, update layout.tsx |
| 2.7 | Update Next.js configuration | Not Started | - | Remove i18n routing from next.config.ts |
| 2.8 | Remove language parameters from API calls | Not Started | - | Update WebSocket calls and HTTP requests |
| 2.9 | Clean up utility functions and hooks | Not Started | - | Remove language-related utilities |
| 2.10 | Final testing and validation | Not Started | - | Ensure all functionality works with English-only |

## Progress Log
### 2025-01-28
- Created task after comprehensive codebase analysis
- Identified all components of the internationalization system
- Developed systematic approach for removal while maintaining functionality
- Estimated this as a significant refactoring affecting ~20+ files

## Technical Considerations
- **Breaking Changes**: This will be a breaking change for any non-English users
- **Testing Required**: Comprehensive testing needed to ensure no functionality is lost
- **Code Quality**: Opportunity to simplify and clean up the codebase
- **Performance**: Should result in smaller bundle size and faster load times
- **Maintenance**: Reduced complexity for future development

## Risk Assessment
- **Low Risk**: Most changes are straightforward removals
- **Medium Risk**: Need to ensure all translation string replacements are accurate
- **Testing Critical**: Must verify that removing language context doesn't break any functionality

## Files to be Modified/Removed
### Removed Files (9):
- `src/i18n.ts`
- `src/messages/en.json`
- `src/messages/es.json`
- `src/messages/fr.json`
- `src/messages/ja.json`
- `src/messages/kr.json`
- `src/messages/pt-br.json`
- `src/messages/ru.json`
- `src/messages/vi.json`
- `src/messages/zh-tw.json`
- `src/messages/zh.json`
- `src/contexts/LanguageContext.tsx`
- `api/config/lang.json`

### Modified Files (~15):
- `src/app/layout.tsx`
- `src/components/ConfigurationModal.tsx`
- `src/components/Ask.tsx`
- `src/components/ModelSelectionModal.tsx`
- `src/components/TokenInput.tsx`
- `src/components/WikiTypeSelector.tsx`
- `src/components/UserSelector.tsx`
- `src/app/page.tsx`
- `src/app/[owner]/[repo]/page.tsx`
- `api/websocket_wiki.py`
- `api/rag.py`
- `api/api.py`
- `next.config.ts`
- `src/hooks/useProcessedProjects.ts`
- Additional utility files as discovered