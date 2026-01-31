import { useState } from 'react';
import VerseDisplay from '../components/VerseDisplay';
import ChatInterface from '../components/ChatInterface';
import LexiconPanel from '../components/LexiconPanel';
import { useAuth } from '../hooks';

type TabType = 'verse' | 'chat' | 'lexicon';

const Dashboard = () => {
  const [selectedStrongsNumber, setSelectedStrongsNumber] = useState<string | undefined>();
  const [selectedGreekWord, setSelectedGreekWord] = useState<string | undefined>();
  const [currentVerseReference, setCurrentVerseReference] = useState<string | undefined>();
  const [activeTab, setActiveTab] = useState<TabType>('verse');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { logout, user } = useAuth();

  const handleWordClick = (strongsNumber: string, greekWord: string) => {
    setSelectedStrongsNumber(strongsNumber);
    setSelectedGreekWord(greekWord);
  };

  const handleVerseLoaded = (reference: string) => {
    setCurrentVerseReference(reference);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex items-center justify-between">
            <div className="min-w-0 flex-1">
              <h1 className="text-lg sm:text-2xl font-bold text-gray-900 truncate">
                AI Gospel Parser
              </h1>
              <p className="text-xs sm:text-sm text-gray-600 mt-0.5 sm:mt-1 hidden sm:block">
                Greek New Testament Study Tool
              </p>
            </div>
            <div className="flex items-center gap-2 sm:gap-4">
              {user && (
                <span className="text-xs sm:text-sm text-gray-600 hidden md:inline truncate max-w-[150px]">
                  {user.full_name || user.email}
                </span>
              )}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 text-gray-600 hover:text-gray-900 touch-manipulation"
                aria-label="Menu"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {mobileMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
              <button
                onClick={logout}
                className="hidden md:block text-gray-600 hover:text-gray-900 text-sm font-medium hover:underline touch-manipulation"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Mobile Menu Dropdown */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-3 pt-3 border-t">
              <div className="space-y-2">
                {user && (
                  <div className="px-3 py-2 text-sm text-gray-600 bg-gray-50 rounded">
                    {user.full_name || user.email}
                  </div>
                )}
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50 rounded touch-manipulation"
                >
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Mobile Tabs - Only visible on small screens */}
      <div className="lg:hidden bg-white border-b sticky top-[60px] sm:top-[72px] z-30">
        <div className="container mx-auto">
          <div className="flex">
            <button
              onClick={() => setActiveTab('verse')}
              className={`flex-1 px-4 py-3 text-sm font-medium touch-manipulation ${
                activeTab === 'verse'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              📖 Verse
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 px-4 py-3 text-sm font-medium touch-manipulation ${
                activeTab === 'chat'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              💬 AI Chat
            </button>
            <button
              onClick={() => setActiveTab('lexicon')}
              className={`flex-1 px-4 py-3 text-sm font-medium touch-manipulation ${
                activeTab === 'lexicon'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              📚 Lexicon
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-3 sm:px-4 py-4 sm:py-6">
        {/* Desktop: 3-column grid */}
        <div className="hidden lg:grid lg:grid-cols-3 gap-6">
          {/* Verse Display - Left Column */}
          <div className="lg:col-span-1">
            <VerseDisplay
              onWordClick={handleWordClick}
              onVerseLoaded={handleVerseLoaded}
            />
          </div>

          {/* Chat Interface - Middle Column */}
          <div className="lg:col-span-1">
            <ChatInterface verseReference={currentVerseReference} />
          </div>

          {/* Lexicon Panel - Right Column */}
          <div className="lg:col-span-1">
            <LexiconPanel
              strongsNumber={selectedStrongsNumber}
              greekWord={selectedGreekWord}
            />
          </div>
        </div>

        {/* Mobile: Tab-based single column */}
        <div className="lg:hidden">
          {activeTab === 'verse' && (
            <VerseDisplay
              onWordClick={(strongs, greek) => {
                handleWordClick(strongs, greek);
                setActiveTab('lexicon'); // Auto-switch to lexicon on word click
              }}
              onVerseLoaded={handleVerseLoaded}
            />
          )}
          {activeTab === 'chat' && (
            <ChatInterface verseReference={currentVerseReference} />
          )}
          {activeTab === 'lexicon' && (
            <LexiconPanel
              strongsNumber={selectedStrongsNumber}
              greekWord={selectedGreekWord}
            />
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-8 py-4 border-t bg-white">
        <div className="container mx-auto px-3 sm:px-4 text-center text-xs sm:text-sm text-gray-600">
          <p className="hidden sm:block">AI Gospel Parser - Greek New Testament Study Tool</p>
          <p className="mt-1">
            <span className="hidden sm:inline">Click Greek words to see lexicon entries • Ask the AI questions about the text</span>
            <span className="sm:hidden">Click words → Lexicon • Ask AI questions</span>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
